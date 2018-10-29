#include <iostream>

using namespace std;

#include "geo.h"

int main()
{
    geo::TRational r(-12, 4);
    geo::TPoint p( geo::TRational(1,3), geo::TRational(3,1));
    cout << "Hello World " << p.getX() << " " << sizeof p << endl;
    return 0;
}
