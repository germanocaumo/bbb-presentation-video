# SPDX-FileCopyrightText: 2024 BigBlueButton Inc. and by respective authors
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from math import tau
from typing import TypeVar

import cairo
import perfect_freehand

from bbb_presentation_video.renderer.tldraw.shape import (
    HighlighterShape,
    apply_shape_rotation,
)
from bbb_presentation_video.renderer.tldraw.utils import draw_smooth_stroke_point_path
from bbb_presentation_video.renderer.tldraw.v2.utils import (
    FONT_SIZES,
    HIGHLIGHT_COLORS,
    rng,
)

CairoSomeSurface = TypeVar("CairoSomeSurface", bound=cairo.Surface)

# From tldraw shapes/highlight/HighlightShapeUtil.mjs. tldraw also draws an underlay
# with 0.82 opacity behind all shapes, which the slide covers.
OVERLAY_OPACITY: float = 0.35


def finalize_highlight(
    ctx: cairo.Context[CairoSomeSurface], id: str, shape: HighlighterShape
) -> None:
    print(f"\tTldraw: Finalizing Highlight: {id}")

    apply_shape_rotation(ctx, shape)

    style = shape.style
    stroke = HIGHLIGHT_COLORS[style.color]
    stroke_width = FONT_SIZES[style.size] * 1.12

    if len(shape.points) == 1:
        # tldraw draws a single point as a dot with a slightly random size
        if not shape.is_pen:
            stroke_width += rng(id)() * (stroke_width / 6)
        point = shape.points[0]
        ctx.arc(point[0], point[1], 0.1, 0, tau)
    else:
        stroke_points = perfect_freehand.get_stroke_points(
            shape.points, size=1 + stroke_width, streamline=0.5, last=shape.isComplete
        )
        draw_smooth_stroke_point_path(ctx, stroke_points, closed=False)

    ctx.set_line_cap(cairo.LineCap.ROUND)
    ctx.set_line_join(cairo.LineJoin.ROUND)
    ctx.set_line_width(stroke_width)
    ctx.set_source_rgba(stroke.r, stroke.g, stroke.b, OVERLAY_OPACITY * style.opacity)
    ctx.stroke()
