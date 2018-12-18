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

    return 0;
}
