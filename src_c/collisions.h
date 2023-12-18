#ifndef _PG_COLLISIONS_H
#define _PG_COLLISIONS_H

#include "geometry.h"

static inline int
pgCollision_CirclePoint(pgCircleBase *circle, double, double);

static inline int
pgCollision_CircleCircle(pgCircleBase *, pgCircleBase *);

static inline int
pgCollision_RectCircle(double rx, double ry, double rw, double rh,
                       pgCircleBase *circle);

#endif /* ~_PG_COLLISIONS_H */
