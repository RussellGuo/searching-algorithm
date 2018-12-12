#ifndef FIGURE_H
#define FIGURE_H

#include "geo.h"
#include <vector>

namespace geo {
class Figure
{
public:
    Figure():lines() {}
    Figure(const Figure &parent, const Line &ll):lines(parent.lines) {
        lines.push_back(ll);
        std::sort(lines.begin(), lines.end());
        lines.shrink_to_fit();
    }

    const std::vector<Line> &getLines() const {
        return lines;
    }
    size_t lineCount() const {
        auto ret = lines.size();
        return ret;
    }

    Figure(const Figure &fig):lines(fig.lines) {}
    Figure& operator =(const Figure &) = delete;

    typedef const Figure *FigurePtr;

    bool operator ==(const Figure &other) const { return lines == other.lines;}

    struct hash {
        size_t operator() (const Figure &fig) const {
            size_t ret;
            ret = 0;
            Line::hash hash;
            for (auto line:fig.lines) {
                auto a = hash(line);
                ret *= 97;
                ret += a;
            }
            return ret;
        }
    };
    struct pointHash {
        size_t operator() (const FigurePtr &fig) const {
            size_t ret = hash()(*fig);
            return ret;
        }
    };
    struct pointEqual {
        bool operator() (const FigurePtr &fig_left, const FigurePtr &fig_right) const {
            bool ret = *fig_left == *fig_right;
            return ret;
        }
    };
    struct pointLess {
        bool operator() (const FigurePtr &fig_left, const FigurePtr &fig_right) const {
            if (fig_left->lineCount() != fig_right->lineCount()) {
                return fig_left->lineCount() < fig_right->lineCount();
            }
            for (unsigned i = 0; i < fig_left->lineCount(); i++) {
                if (fig_left->getLines()[i] != fig_right->getLines()[i]) {
                    return fig_left->getLines()[i] < fig_right->getLines()[i];
                }
            }
            return false;
        }
    };

private:
    std::vector<Line> lines;
};

typedef std::set<Figure::FigurePtr, Figure::pointLess> FigSet;

void testFigure();


}
#endif // FIGURE_H
