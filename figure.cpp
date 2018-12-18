#include "figure.h"

using namespace geo;

void geo::testFigure()
{
    FigSet set;
    Figure nullFig;
    Line line1(1, 0, 1), line2(0, 1, Rational(1, 2));

    Figure fig1(nullFig, line1);
    Figure fig2(fig1, line2);
    Figure fig3(nullFig, line2);
    Figure fig4(fig3, line1);
    auto ret1 = set.insert(nullFig);
    auto ret2 = set.insert(nullFig);
    auto ret3 = set.insert(fig1);
    auto cmp = fig2 == fig4;

    auto it = set.cbegin();
    *it;
}


