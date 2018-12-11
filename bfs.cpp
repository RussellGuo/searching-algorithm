#include <unordered_map>
#include <boost/range/join.hpp>
#include "bfs.h"

#include "figure.h"
using namespace geo;

bfs::bfs(const unsigned max_level)
{
    typedef std::vector<Figure::FigurePtr> FigList;
    typedef std::unordered_map<Point, FigList, Point::hash> MapForPointToFig;

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
    FigSet fig_tab(10000 * 10000U);
    fig_tab.insert(init_fig);

    MapForPointToFig point_fig_map(700 * 10000U);
    for (const auto &p: init_points) {
        auto& fig_list = point_fig_map[p];
        fig_list.push_back(init_fig);
    }

    size_t count = 0;

    for (size_t level = 0; level <= max_level; level++) {
        std::vector<const Figure*> cur_level_fig_tab;
        for (auto fig:fig_tab) {
            if (fig->lineCount() == level) {
                cur_level_fig_tab.push_back(fig);
            }
        }
        printf("level: %zd, total figures %zd\n", level, cur_level_fig_tab.size());
        if (level == max_level) {
            fig_tab.rehash(0);
        }
        for (const auto cur_fig:cur_level_fig_tab) {
            if (count % 10000 == 0) {
                printf("log:%10zd, ", count);
                printf("%10zd, %10zd\n",
                       cur_level_fig_tab.size(),
                       point_fig_map.size());
            }
            count++;
            // find all the point and record them
            // should use all lines cross (all lines + init_lines)
            PointSet new_points;

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
                    auto ret = new_points.insert(point);
                    if (ret.second) {
                        auto &fig_lst = point_fig_map[point];
                        if (fig_lst.empty() || fig_lst[0]->lineCount() >= level ) {
                            fig_lst.push_back(cur_fig);
                        }
                    }
                }
            }

            if (level == max_level) {
                continue;
            }
            LineSet new_lines(first_level_line_set);
            {
                PointSet all_points(init_points);
                for (const auto &point:new_points) {
                    all_points.insert(point);
                }
                for (const auto& point_1:new_points) {
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
                if (fig_tab.find(&fig) == fig_tab.cend()) {
                    Figure *ptr = new Figure(fig);
                    fig_tab.insert(ptr);
                }
            }

            cur_fig->getLines();
        }
    }

    printf("total:%10zd, %10zd\n", fig_tab.size(), point_fig_map.size());
    std::vector<Figure::FigurePtr>fig_vec(fig_tab.cbegin(), fig_tab.cend());
    Figure::pointLess comp;
    std::sort(fig_vec.begin(), fig_vec.end(), comp);
    for(const auto& f:fig_vec) {
        const auto& lines = f->getLines();
        for (const auto &line: lines) {
            Int a, b, c;
            line.getParams(a, b, c);
            printf("%d %d %d  ", a, b, c);
        }
        printf("\n");
    }

}

