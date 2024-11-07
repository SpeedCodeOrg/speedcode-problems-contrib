#include "solution.hpp"
#include <optional>
#include <string>
#include <nanobench.h>
#include <sstream>
#include <memory>
#include <vector>
#include "solution_ref.hpp"

#include <iostream>
#include <fstream>
#include <random>

class ProblemInput {
    std::string inp_name;
    quicktype::Inputschema input;
    uint64_t N;
    uint64_t M;
    eidType* rowptr;
    vidType* col;
    weight_type* weights;

    std::vector<vidType> queries;
    std::vector<std::vector<weight_type>> distances;
    BaseGraph* graph;
public:

    void construct_from_coo(std::vector<int64_t>& input_row, std::vector<int64_t>& input_col, std::vector<double>& input_weight) {
        // convert COO form to CSR format.
        N = input_row[0];
        for (int64_t i = input_row.size(); --i >= 0;) {
            if (input_row[i] > N) {
                N = input_row[i];
            }
        }
        M = input_col.size();
        assert(input_col.size() == input_row.size() && "In COO format col and row must have the same lengths");
        assert(input_col.size() == input_weight.size() && "In COO format col, row, weights must have the same lengths");
        rowptr = new eidType[N+1]();
        col = new vidType[M]();
        weights = new weight_type[M]();

        for (size_t i = 0; i < input_row.size(); i++) {
            vidType src = input_row[i];
            vidType dst = input_col[i]; 
            col[i] = dst;
            rowptr[src] += 1;
            weights[i] = input_weight[i];
        }
        for (size_t i = 1; i < N+1; i++) {
            rowptr[i] += rowptr[i-1];
        }
    }

    void construct_from_file(std::string& filename) {
        //std::ifstream s{filename, s.trunc | s.in | s.out | s.binary};
        std::string path = Driver::get_datafile_path(filename);
        std::ifstream s{path, s.in | s.binary};
        
        s.read((char*)&N, sizeof(decltype(N)));
        s.read((char*)&M, sizeof(decltype(M)));

        rowptr = (decltype(rowptr)) malloc(sizeof(eidType)*(N+1));
        col = (decltype(col)) malloc(sizeof(vidType)*M);
        weights = (decltype(weights)) malloc(sizeof(weight_type)*M);

        s.read((char*)rowptr, sizeof(eidType)*(N+1));
        s.read((char*)col, sizeof(vidType)*M);
        s.read((char*)weights, sizeof(weight_type)*M);
        s.close();
        printf("Successfully deserialized the data. %d, %d\n", N, M);
    }

    ProblemInput(std::string inp_name, quicktype::Inputschema& _input, decltype(initialize_graph) init = initialize_graph) {
        inp_name = inp_name;
        input = _input;
        if (_input.graph.data_file_format.has_value()) {//filename.has_value()) {
            assert(_input.graph.filename.has_value() && _input.graph.file_format.has_value());
            assert(_input.graph.file_format.value() == "binary"); // update if there are more file formats.
            construct_from_file(_input.graph.filename.value());
        } else if (_input.graph.coo_format.has_value()) {
            assert(_input.graph.row.has_value() && _input.graph.col.has_value() &&
                   _input.graph.weight.has_value() && "COO values missing.");
            construct_from_coo(_input.graph.row.value(), _input.graph.col.value(), _input.graph.weight.value());
        } else if (_input.graph.random_generated_graph.has_value()) {
            generate_random_graph(_input.graph.num_vertices.value(), _input.graph.num_edges_per_vertex.value());
        } else {
            assert(false && "Error no valid format\n");
        }

        // Helper function to convert formats to binary format.
        // NOTE: The serialize function will not replace existing files with the same name in the data/ directory.
        if (_input.meta_info.has_value()) {
           auto meta_info = _input.meta_info.value();
           if (meta_info.save_to_binary) {
              serialize(meta_info.save_filename);
           } 
        }

        graph = init(rowptr, col, weights, N, M);
        
        for (int i = 0; i < 1; i++) {
            queries.push_back(i);
            distances.emplace_back(N, std::numeric_limits<weight_type>::max());
        }
    }


    void generate_random_graph(int64_t num_vertices, int64_t num_edges_per_vertex) {
        std::random_device r;
        std::default_random_engine el(r());
        std::uniform_int_distribution<uint64_t> uniform_dist(0,num_vertices);
        std::uniform_real_distribution<float> uniform_weight_dist(0,10.0);
        int64_t num_edges = num_vertices * num_edges_per_vertex;
        std::vector<std::tuple<int64_t, int64_t, float>> edges;
        edges.reserve(num_edges);
        for (int64_t i = 0; i < num_edges; i++) {
            uint64_t src = uniform_dist(el);
            uint64_t dst = uniform_dist(el);
            if (src == dst) continue;
            float weight = uniform_weight_dist(el); 
            edges.push_back(std::make_tuple(src,dst,weight));
            edges.push_back(std::make_tuple(dst,src,weight));
        }
        std::sort(edges.begin(), edges.end());
        std::vector<std::tuple<int64_t, int64_t, float>> filtered_edges;
        filtered_edges.reserve(edges.size());
        for (int64_t i = 0; i < edges.size(); i++) {
            if (i == 0 || std::get<0>(edges[i]) != std::get<0>(edges[i-1]) ||
                 std::get<1>(edges[i]) != std::get<1>(edges[i-1])) {
               filtered_edges.push_back(edges[i]); 
            }
        }
        std::vector<int64_t> row(filtered_edges.size());
        std::vector<int64_t> col(filtered_edges.size());
        std::vector<double> weights(filtered_edges.size());
        for (int64_t i = 0; i < filtered_edges.size(); i++) {
            row[i] = std::get<0>(filtered_edges[i]);
            col[i] = std::get<1>(filtered_edges[i]);
            weights[i] = std::get<2>(filtered_edges[i]);
        }
        construct_from_coo(row, col, weights);
    }

    void serialize(std::string name) {
        std::string filename = Driver::get_datafile_path(name);//"test.bin";
        if(std::ifstream(filename.c_str()).good()) {
            printf("Data file already exists, skipping\n");
            return;
        }
        std::ofstream s{filename, s.trunc | s.in | s.out | s.binary};
        s.write((char*)&N, sizeof(decltype(N)));
        s.write((char*)&M, sizeof(decltype(M)));
        s.write((char*)rowptr, sizeof(eidType)*(N+1));
        s.write((char*)col, sizeof(vidType)*M);
        s.write((char*)weights, sizeof(weight_type)*M);
        s.close(); 
    }

    void deserialize() {
        std::string filename = "test.bin";
        std::ifstream s{filename, s.in | s.binary};
        
        s.read((char*)&N, sizeof(decltype(N)));
        s.read((char*)&M, sizeof(decltype(M)));

        rowptr = (decltype(rowptr)) malloc(sizeof(eidType)*(N+1));
        col = (decltype(col)) malloc(sizeof(vidType)*M);
        weights = (decltype(weights)) malloc(sizeof(weight_type)*M);

        s.read((char*)rowptr, sizeof(eidType)*(N+1));
        s.read((char*)col, sizeof(vidType)*M);
        s.read((char*)weights, sizeof(weight_type)*M);
        s.close();
        printf("Successfully deserialized the data. %d, %d\n", N, M);
    }

    // old test function.
    void deserialize_test() {
        std::string filename = "test.bin";
        std::ifstream s{filename, s.in | s.binary};
        decltype(N) N_test;
        decltype(M) M_test;
        decltype(rowptr) rowptr_test;
        decltype(col) col_test;
        decltype(weights) weights_test;
        
        s.read((char*)&N_test, sizeof(decltype(N)));
        s.read((char*)&M_test, sizeof(decltype(M)));

        assert(N == N_test && "N != N_test");
        assert(M == M_test && "N != N_test");

        rowptr_test = (decltype(rowptr)) malloc(sizeof(eidType)*(N_test+1));
        col_test = (decltype(col)) malloc(sizeof(vidType)*M_test);
        weights_test = (decltype(weights)) malloc(sizeof(weight_type)*M_test);

        s.read((char*)rowptr_test, sizeof(eidType)*(N_test+1));
        s.read((char*)col_test, sizeof(vidType)*M_test);
        s.read((char*)weights_test, sizeof(weight_type)*M_test);
        s.close();
        for (int64_t i = 0; i < N_test+1; i++) {
            assert(rowptr_test[i] == rowptr[i] && "Rowptr doesn't match");
        }
        for (int64_t i = 0; i < M_test; i++) {
            assert(col_test[i] == col[i] && "Col doesn't match.");
            assert(weights_test[i] == weights[i] && "weights doesn't match.");
        }
        printf("Successfully deserialized the data. %d, %d\n", N_test, M_test);
    }

    ~ProblemInput() {
        delete[] rowptr;
        delete[] col;
        delete[] weights;
        delete graph;
    }

    auto run() {
        for (int i = 0; i < queries.size(); i++) {
            graph->SSSP(queries[i], distances[i].data());
        }
        return true;
    }

    bool approximatelyEqual(weight_type a, weight_type a_ref, double absError = 1e-7, double relError = 1e-9) {
        if (fabs(a-a_ref) <= absError || fabs(a-a_ref) <= a_ref*relError) return true;
        return false;
    }

    std::optional<std::string> check() {
        ProblemInput reference = ProblemInput(inp_name, input, reference::initialize_graph);
        run();
        reference.run();
        for (int64_t i = 0; i < distances.size(); i++) {
            if (distances[i].size() != reference.distances[i].size()) return "Incorrect # queries in distance array";
            for (int64_t j = 0; j < distances[i].size(); j++) {
                if (!approximatelyEqual(distances[i][j], reference.distances[i][j])) {
                    return "Incorrect value, expected distance " + std::to_string(reference.distances[i][j]) + ", but got " + std::to_string(distances[i][j]);
                }
            }
        }
        return std::nullopt;
    }
};
