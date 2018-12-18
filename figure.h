#ifndef FIGURE_H
#define FIGURE_H

#include "geo.h"
#include <vector>

namespace geo {
class Figure: private std::vector<Line>
{
public:
    Figure() {}
    Figure(const Figure &parent, const Line &ll):vector(parent) {
        push_back(ll);
        std::sort(begin(), end());
        shrink_to_fit();
    }

    const std::vector<Line> &getLines() const {
        return *this;
    }
    size_t lineCount() const {
        auto ret = size();
        return ret;
    }

    void setEightSymmetry(Figure symmetryArray[8]) const {
        uint16_t line_count = uint16_t(lineCount());
        for (uint16_t i = 0; i < 8; i++) {
            symmetryArray[i].resize(line_count);
        }
        Line LineArray[8];
        for (uint16_t ll = 0; ll < line_count; ll++) {
            (*this)[ll].setEightSymmetry(LineArray);
            for (uint16_t i = 0; i < 8; i++) {
                symmetryArray[i][ll] =LineArray[i];
            }
        }
        for (uint16_t i = 0; i < 8; i++) {
            std::sort(symmetryArray[i].begin(), symmetryArray[i].end());
        }
    }

    Figure(const Figure &fig) = default;
    Figure& operator =(const Figure &) = delete;

    bool operator ==(const Figure &other) const { return vector(*this) == other;}
    bool operator <(const Figure &other) const {
        if (lineCount() == other.lineCount()) {
            for (uint16_t i = 0; i < lineCount(); i++) {
                if ((*this)[i] != other[i]) {
                    return (*this)[i] < other[i];
                }
            }
            return false;
        } else {
            return lineCount() < other.lineCount();
        }
    }

    struct hash {
        size_t operator() (const Figure &fig) const {
            size_t ret;
            ret = 0;
            Line::hash hash;
            for (auto line:vector(fig)) {
                auto a = hash(line);
                ret *= 97;
                ret += a;
            }
            return ret;
        }
    };

};

typedef std::set<Figure> FigSet;

void testFigure();


}
#endif // FIGURE_H
