#ifndef BFS_H
#define BFS_H

#include "figure.h"
#include <forward_list>
using namespace geo;

class bfs
{
public:
    explicit bfs();
    void searching(const unsigned max_level = 3);
    void output_point_figure_symmetry(const Figure &fig, const PointSet& points);
    void output_point_figure(const Figure &fig, const PointSet& points);

    const std::forward_list<std::pair<Figure, Point>> getOutput() const {
        return output;
    }

private:
    LineSet init_lines;
    PointSet init_points;
    LineSet first_level_line_set;

    std::forward_list<std::pair<Figure, Point>> output;

};

#endif // BFS_H
