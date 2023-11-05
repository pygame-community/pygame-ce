#ifndef _PG_COLLISIONS_H
#define _PG_COLLISIONS_H

#include "geometry.h"

static int
pgCollision_CirclePoint(pgCircleBase *circle, double, double);

static int
pgCollision_CircleCircle(pgCircleBase *, pgCircleBase *);

#endif /* ~_PG_COLLISIONS_H */
