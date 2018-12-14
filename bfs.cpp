#include <set>
#include <map>
#include <forward_list>
#include <unordered_map>

#include <boost/range/join.hpp>
#include <boost/date_time/posix_time/posix_time.hpp>

#include "bfs.h"
#include "figure.h"
using namespace geo;

inline static void output_point_figure(const Figure::FigurePtr &fig_ptr, const PointSet& points)
{
    if (points.size() <= 0) {
        return;
    }
    for (const auto &line: fig_ptr->getLines()) {
        Int a, b, c;
        line.getParams(a, b, c);
        fprintf(stderr, "%d %d %d ", a, b, c);
    }
    fprintf(stderr, "0 0 0 ");

    for (const auto &point: points) {
        auto x(point.getX()), y(point.getY());
        fprintf(stderr, "%d %d %d %d ", x.numerator(), x.denominator(), y.numerator(), y.denominator());
    }
    fprintf(stderr, "0 0 0 0\n");
}

bfs::bfs(const unsigned max_level)
{
    const auto begin_time = boost::posix_time::microsec_clock::local_time();

    LineSet init_lines;
    for (auto i = -geo::MAX_GRID_COORD; i <= geo::MAX_GRID_COORD; i++) {
        init_lines.emplace(1, 0, i);
        init_lines.emplace(0, 1, i);
    }

    PointSet init_points;
    for(const auto &line1:init_lines) {
        for (const auto &line2:init_lines) {
            if (line1 < line2) {
                Point point;
                if (Line::getIntersectionPoint(line1, line2, point)) {
                    init_points.insert(point);
                }
            }
        }
    }

    LineSet first_level_line_set;
    for (const auto &point1:init_points){
        for (const auto &point2:init_points) {
            if (point1 < point2) {
                Line line(point1, point2);
                if (line.isValid()) {
                    if (init_lines.find(line) == init_lines.cend()) { // not in level 0 lines.
                        first_level_line_set.insert(line);
                    }
                }
            }
        }
    }

    Figure *init_fig = new Figure();
    FigSet cur_level_fig_tab;
    cur_level_fig_tab.insert(init_fig);
    output_point_figure(init_fig, init_points);

    PointSet low_level_point_set(init_points);

    size_t count = 0;

    for (size_t level = 0; level <= max_level; level++) {
        PointSet cur_level_point_set;
        FigSet next_level_fig_tab;
        printf("level: %zd, total figures %zd\n", level, cur_level_fig_tab.size());
        for(const auto cur_fig:cur_level_fig_tab) {
            if (count % 10000 == 0) {
                const auto microsec = boost::posix_time::microsec_clock::local_time() - begin_time;
                printf("log:%10zd, %10ld\n", count, microsec.total_microseconds());
                fflush(stdout);
            }
            count++;
            // find all the point and record them
            // should use all lines cross (all lines + init_lines)
            PointSet cur_fig_points_other_than_init_fig;
            PointSet cur_fig_points_for_cur_level;

            const auto &line_vector(cur_fig->getLines());
            LineSet geo_lines(line_vector.cbegin(), line_vector.cend());
            LineSet all_lines(init_lines);
            for (const auto &line:line_vector) {
                all_lines.insert(line);
            }

            Point point;
            for(const auto &line_a:geo_lines) {
                for (const auto &line_b:all_lines) {
                    if (!Line::getIntersectionPoint(line_a, line_b, point)) {
                        continue;
                    }
                    auto inserted = cur_fig_points_other_than_init_fig.insert(point).second;
                    if (inserted && low_level_point_set.find(point) == low_level_point_set.end()) {
                        cur_fig_points_for_cur_level.insert(point);
                    }
                }
            }
            output_point_figure(cur_fig, cur_fig_points_for_cur_level);

            if (level == max_level) {
                continue;
            }
            for (const auto &p:cur_fig_points_for_cur_level) {
                cur_level_point_set.insert(p);
            }
            LineSet new_lines(first_level_line_set);
            {
                PointSet all_points(init_points);
                for (const auto &point:cur_fig_points_other_than_init_fig) {
                    all_points.insert(point);
                }
                for (const auto& point_1:cur_fig_points_other_than_init_fig) {
                    for(const auto& point_2: all_points) {
                        Line line(point_1, point_2);
                        if (!line.isValid()) {
                            continue;
                        }
                        new_lines.insert(line);
                    }
                }
            }
            for(const auto &line: new_lines) {
                if (all_lines.find(line) != all_lines.cend()) {
                    continue;
                }
                Figure fig(*cur_fig, line);
                if (next_level_fig_tab.find(&fig) == next_level_fig_tab.cend()) {
                    Figure *ptr = new Figure(fig);
                    next_level_fig_tab.insert(ptr);
                }
            }

            cur_fig->getLines();
        }
        {
            swap(low_level_point_set, cur_level_point_set);
            for (const auto &p:cur_level_point_set) {
                low_level_point_set.insert(p);
            }
        }
        cur_level_fig_tab.clear();
        swap(cur_level_fig_tab, next_level_fig_tab);

    }
}

