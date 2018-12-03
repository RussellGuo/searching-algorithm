#ifndef FIGURE_H
#define FIGURE_H

#include "geo.h"
#include <vector>

namespace geo {
class Figure
{
public:
    Figure():lines() {}
    Figure(const Figure &parent, Line &ll):lines(parent.lines) { lines.push_back(ll); std::sort(lines.begin(), lines.end()); }
    Figure(const Figure &) = delete;
    Figure& operator =(const Figure &) = delete;

    bool operator ==(const Figure & other) { return lines == other.lines;}
    struct Hash {
        size_t operator() (const Figure &fig) {
            size_t ret;
            ret = 0;
            Line::Hash hash;
            for (auto line:fig.lines) {
                auto a = hash(line);
                ret *= 97;
                ret += a;
            }
            return ret;
        }
    };

private:
    std::vector<Line> lines;
};

}
#endif // FIGURE_H
