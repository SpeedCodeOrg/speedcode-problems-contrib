//  To parse this JSON data, first install
//
//      json.hpp  https://github.com/nlohmann/json
//
//  Then include this file, and then do
//
//     Inputschema data = nlohmann::json::parse(jsonString);

#pragma once

#include <nlohmann/json.hpp>

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

    struct Inputschema {
        std::vector<int64_t> col;
        std::vector<int64_t> row;
        std::vector<double> weight;
    };
}

namespace quicktype {
    void from_json(const json & j, Inputschema & x);
    void to_json(json & j, const Inputschema & x);

    inline void from_json(const json & j, Inputschema& x) {
        x.col = j.at("col").get<std::vector<int64_t>>();
        x.row = j.at("row").get<std::vector<int64_t>>();
        x.weight = j.at("weight").get<std::vector<double>>();
    }

    inline void to_json(json & j, const Inputschema & x) {
        j = json::object();
        j["col"] = x.col;
        j["row"] = x.row;
        j["weight"] = x.weight;
    }
}
