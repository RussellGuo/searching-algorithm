
#include <chrono>

#include "bfs.h"
#include "figure.h"
using namespace geo;

inline void bfs::output_point_figure(const Figure &fig, const PointSet& points)
{
    if (points.size() <= 0) {
        return;
    }
    for (const auto &line: fig.getLines()) {
        Int a, b, c;
        line.getParams(a, b, c);
        printf("%d %d %d ", a, b, c);
    }
    printf("0 0 0 ");

    for (const auto &point: points) {
        auto x(point.getX()), y(point.getY());
        printf("%d %d %d %d ", x.numerator(), x.denominator(), y.numerator(), y.denominator());
    }
    printf("0 0 0 0\n");
}

inline void bfs::output_point_figure_symmetry(const Figure &fig, const PointSet& points)
{
    if (points.size() == 0) {
        return;
    }
    for (const auto &point: points) {
        output.push_front(std::make_pair(fig, point));
    }
    return;

    Figure fig_symmetry_array[8];
    PointSet points_symmetry_array[8];
    fig.setEightSymmetry(fig_symmetry_array);
    for (const auto &point: points) {
        Point point_sysmmetry_array[8];
        point.setEightSymmetry(point_sysmmetry_array);
        for (uint16_t i = 0; i < 8; i++) {
            points_symmetry_array[i].insert(point_sysmmetry_array[i]);
        }
    }

    for (uint16_t i = 0; i < 8; i++) {
        output_point_figure(fig_symmetry_array[i], points_symmetry_array[i]);
    }
}

bfs::bfs()
{

    for (auto i = -geo::MAX_GRID_COORD; i <= geo::MAX_GRID_COORD; i++) {
        init_lines.emplace(1, 0, i);
        init_lines.emplace(0, 1, i);
    }

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
}

void bfs::searching(const unsigned max_level)
{
    const auto begin_time = std::chrono::steady_clock::now();

    output.clear();
    Figure init_fig;
    FigSet cur_level_fig_tab;
    cur_level_fig_tab.insert(init_fig);
    output_point_figure_symmetry(init_fig, init_points);

    PointSet low_level_point_set(init_points);

    size_t count = 0;

    for (size_t level = 0; level <= max_level; level++) {
        PointSet cur_level_point_set;
        FigSet next_level_fig_tab;
        fprintf(stderr, "level: %zd, total figures %zd, low level points %zd\n", level, cur_level_fig_tab.size(), low_level_point_set.size());
        for(const auto &cur_fig:cur_level_fig_tab) {
            if (count % 10000 == 0) {
                const auto nanosec = std::chrono::steady_clock::now() - begin_time;
                fprintf(stderr, "log:%10zd, %10lds\n", count, nanosec.count() / 1000000000);
                fflush(stderr);
            }
            count++;
            // find all the point and record them
            // should use all lines cross (all lines + init_lines)
            PointSet cur_fig_points_other_than_init_fig;
            PointSet cur_fig_points_for_cur_level;

            const auto &line_vector(cur_fig.getLines());
            LineSet geo_lines(line_vector.cbegin(), line_vector.cend());
            LineSet all_lines(init_lines);
            std::copy(line_vector.begin(), line_vector.end(), std::inserter(all_lines, all_lines.begin()));

            auto new_points_for_cur_fig = [&cur_fig_points_other_than_init_fig, &cur_fig_points_for_cur_level, &low_level_point_set] (const Point &point) {
                if (!point.isValid()) {
                    return;
                }
                auto inserted = cur_fig_points_other_than_init_fig.insert(point).second;
                if (inserted) {
                    Point symmetryRegularPoint;
                    point.symmetryRegular(symmetryRegularPoint);
                    if (low_level_point_set.find(symmetryRegularPoint) == low_level_point_set.end()) {
                        cur_fig_points_for_cur_level.insert(point);
                    }
                }
            };
            for(const auto &line_a:geo_lines) {
                Int a, b, c;
                line_a.getParams(a, b, c);
                if (a != 0) {
                    for (auto k = -MAX_GRID_COORD; k <= +MAX_GRID_COORD; k++) {
                        Rational x(c - b * k, a);
                        Point p(x, k);
                        new_points_for_cur_fig(p);
                    }

                }
                if (b != 0) {
                    for (auto k = -MAX_GRID_COORD; k <= +MAX_GRID_COORD; k++) {
                        Rational y(c - a * k, b);
                        Point p(k, y);
                        new_points_for_cur_fig(p);
                    }

                }
            }
            for (uint16_t i = 0; i < cur_fig.lineCount(); i++) {
                const auto &line_a = line_vector[i];
                for (uint16_t j = i + 1; j <cur_fig.lineCount(); j++) {
                    const auto &line_b = line_vector[j];
                    Point point;
                    if (Line::getIntersectionPoint(line_a, line_b, point)) {
                        new_points_for_cur_fig(point);
                    }
                }
            }
            output_point_figure_symmetry(cur_fig, cur_fig_points_for_cur_level);

            if (level == max_level) {
                continue;
            }
            for (const auto &p:cur_fig_points_for_cur_level) {
                Point symmetryRegularPoint;
                p.symmetryRegular(symmetryRegularPoint);
                cur_level_point_set.insert(symmetryRegularPoint);
            }
            LineSet new_lines(first_level_line_set);
            {
                auto get_new_line_by_two_points = [&new_lines, &all_lines] (const Point &point_1, const Point &point_2) {
                    Line line(point_1, point_2);
                    if (line.isValid() && all_lines.find(line) == all_lines.cend()) {
                        new_lines.insert(line);
                    }
                };
                for (const auto& point_1:cur_fig_points_other_than_init_fig) {
                    for(const auto& point_2: init_points) {
                        get_new_line_by_two_points(point_1, point_2);
                    }
                }
                for (auto point_1_ptr = cur_fig_points_other_than_init_fig.cbegin(); point_1_ptr != cur_fig_points_other_than_init_fig.cend(); ++point_1_ptr) {
                    for(auto point_2_ptr = point_1_ptr; ++point_2_ptr != cur_fig_points_other_than_init_fig.cend();) {
                        get_new_line_by_two_points(*point_1_ptr, *point_2_ptr);
                    }
                }
            }
            for(const auto &line: new_lines) {
                Figure fig(cur_fig, line);
                Figure fig_symmetry_array[8];
                fig.setEightSymmetry(fig_symmetry_array);
                auto min_fig = std::min_element(std::begin(fig_symmetry_array), std::end(fig_symmetry_array));
                next_level_fig_tab.emplace(*min_fig);
            }

            cur_fig.getLines();
        }
        {
            swap(low_level_point_set, cur_level_point_set);
            std::copy(cur_level_point_set.cbegin(), cur_level_point_set.cend(), std::inserter(low_level_point_set, low_level_point_set.begin()));
        }
        {
            cur_level_fig_tab.clear();
            swap(cur_level_fig_tab, next_level_fig_tab);
        }

    }
}

