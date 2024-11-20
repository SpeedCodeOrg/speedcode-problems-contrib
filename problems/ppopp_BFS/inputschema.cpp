//  To parse this JSON data, first install
//
//      json.hpp  https://github.com/nlohmann/json
//
//  Then include this file, and then do
//
//     Inputschema data = nlohmann::json::parse(jsonString);

#pragma once

#include <optional>
#include <nlohmann/json.hpp>

#ifndef NLOHMANN_OPT_HELPER
#define NLOHMANN_OPT_HELPER
namespace nlohmann {
    template <typename T>
    struct adl_serializer<std::shared_ptr<T>> {
        static void to_json(json & j, const std::shared_ptr<T> & opt) {
            if (!opt) j = nullptr; else j = *opt;
        }

        static std::shared_ptr<T> from_json(const json & j) {
            if (j.is_null()) return std::make_shared<T>(); else return std::make_shared<T>(j.get<T>());
        }
    };
    template <typename T>
    struct adl_serializer<std::optional<T>> {
        static void to_json(json & j, const std::optional<T> & opt) {
            if (!opt) j = nullptr; else j = *opt;
        }

        static std::optional<T> from_json(const json & j) {
            if (j.is_null()) return std::make_optional<T>(); else return std::make_optional<T>(j.get<T>());
        }
    };
}
#endif

namespace quicktype {
    using nlohmann::json;

    #ifndef NLOHMANN_UNTYPED_quicktype_HELPER
    #define NLOHMANN_UNTYPED_quicktype_HELPER
    inline json get_untyped(const json & j, const char * property) {
        if (j.find(property) != j.end()) {
            return j.at(property).get<json>();
        }
        return json();
    }

    inline json get_untyped(const json & j, std::string property) {
        return get_untyped(j, property.data());
    }
    #endif

    #ifndef NLOHMANN_OPTIONAL_quicktype_HELPER
    #define NLOHMANN_OPTIONAL_quicktype_HELPER
    template <typename T>
    inline std::shared_ptr<T> get_heap_optional(const json & j, const char * property) {
        auto it = j.find(property);
        if (it != j.end() && !it->is_null()) {
            return j.at(property).get<std::shared_ptr<T>>();
        }
        return std::shared_ptr<T>();
    }

    template <typename T>
    inline std::shared_ptr<T> get_heap_optional(const json & j, std::string property) {
        return get_heap_optional<T>(j, property.data());
    }
    template <typename T>
    inline std::optional<T> get_stack_optional(const json & j, const char * property) {
        auto it = j.find(property);
        if (it != j.end() && !it->is_null()) {
            return j.at(property).get<std::optional<T>>();
        }
        return std::optional<T>();
    }

    template <typename T>
    inline std::optional<T> get_stack_optional(const json & j, std::string property) {
        return get_stack_optional<T>(j, property.data());
    }
    #endif

    struct Graph {
        std::optional<std::vector<int64_t>> col;
        std::optional<bool> coo_format;
        std::optional<std::vector<int64_t>> row;
        std::optional<std::vector<double>> weight;
        std::optional<int64_t> num_edges_per_vertex;
        std::optional<int64_t> num_vertices;
        std::optional<bool> random_generated_graph;
        std::optional<bool> data_file_format;
        std::optional<std::string> file_format;
        std::optional<std::string> filename;
    };

    struct MetaInfo {
        std::string save_filename;
        bool save_to_binary;
        std::string short_description;
        std::vector<std::string> tags;
    };

    struct Inputschema {
        Graph graph;
        std::optional<MetaInfo> meta_info;
        std::optional<std::vector<int64_t>> sources;
    };
}

namespace quicktype {
    void from_json(const json & j, Graph & x);
    void to_json(json & j, const Graph & x);

    void from_json(const json & j, MetaInfo & x);
    void to_json(json & j, const MetaInfo & x);

    void from_json(const json & j, Inputschema & x);
    void to_json(json & j, const Inputschema & x);

    inline void from_json(const json & j, Graph& x) {
        x.col = get_stack_optional<std::vector<int64_t>>(j, "col");
        x.coo_format = get_stack_optional<bool>(j, "coo_format");
        x.row = get_stack_optional<std::vector<int64_t>>(j, "row");
        x.weight = get_stack_optional<std::vector<double>>(j, "weight");
        x.num_edges_per_vertex = get_stack_optional<int64_t>(j, "num_edges_per_vertex");
        x.num_vertices = get_stack_optional<int64_t>(j, "num_vertices");
        x.random_generated_graph = get_stack_optional<bool>(j, "random_generated_graph");
        x.data_file_format = get_stack_optional<bool>(j, "data_file_format");
        x.file_format = get_stack_optional<std::string>(j, "file_format");
        x.filename = get_stack_optional<std::string>(j, "filename");
    }

    inline void to_json(json & j, const Graph & x) {
        j = json::object();
        j["col"] = x.col;
        j["coo_format"] = x.coo_format;
        j["row"] = x.row;
        j["weight"] = x.weight;
        j["num_edges_per_vertex"] = x.num_edges_per_vertex;
        j["num_vertices"] = x.num_vertices;
        j["random_generated_graph"] = x.random_generated_graph;
        j["data_file_format"] = x.data_file_format;
        j["file_format"] = x.file_format;
        j["filename"] = x.filename;
    }

    inline void from_json(const json & j, MetaInfo& x) {
        x.save_filename = j.at("save_filename").get<std::string>();
        x.save_to_binary = j.at("save_to_binary").get<bool>();
        x.short_description = j.at("short_description").get<std::string>();
        x.tags = j.at("tags").get<std::vector<std::string>>();
    }

    inline void to_json(json & j, const MetaInfo & x) {
        j = json::object();
        j["save_filename"] = x.save_filename;
        j["save_to_binary"] = x.save_to_binary;
        j["short_description"] = x.short_description;
        j["tags"] = x.tags;
    }

    inline void from_json(const json & j, Inputschema& x) {
        x.graph = j.at("graph").get<Graph>();
        x.meta_info = get_stack_optional<MetaInfo>(j, "meta_info");
        x.sources = get_stack_optional<std::vector<int64_t>>(j, "sources");
    }

    inline void to_json(json & j, const Inputschema & x) {
        j = json::object();
        j["graph"] = x.graph;
        j["meta_info"] = x.meta_info;
        j["sources"] = x.sources;
    }
}
