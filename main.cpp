#include <iostream>

using namespace std;

#include <vector>
#include <unordered_set>
#include "geo.h"
#include "figure.h"
#include "bfs.h"

int main()
{
    geo::Rational r(-12, 4);
    geo::Figure f;
    cout << "Hello World " << sizeof f << endl;
    cout << "Hello World " << sizeof f.getLines()[0] << endl;
    geo::testGeoLine();
    geo::testFigure();

    bfs bfs;

    return 0;
}
