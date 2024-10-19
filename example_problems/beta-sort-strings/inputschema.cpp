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
        std::vector<std::string> strings;
    };
}

namespace quicktype {
    void from_json(const json & j, Inputschema & x);
    void to_json(json & j, const Inputschema & x);

    inline void from_json(const json & j, Inputschema& x) {
        x.strings = j.at("strings").get<std::vector<std::string>>();
    }

    inline void to_json(json & j, const Inputschema & x) {
        j = json::object();
        j["strings"] = x.strings;
    }
}
