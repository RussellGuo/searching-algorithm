#include <iostream>

using namespace std;

#include <vector>
#include <unordered_set>
#include "geo.h"
#include "figure.h"
#include "bfs.h"

int main()
{
    geo::testGeoLine();
    geo::testFigure();

    bfs bfs;
    bfs.searching(3);

    auto out = bfs.getOutput();
    size_t total = 0;
    for (const auto &i:out) {i.second.isValid();
        total++;
    }
    printf("count = %zd\n", total);
    { getchar(); }

    return 0;
}
