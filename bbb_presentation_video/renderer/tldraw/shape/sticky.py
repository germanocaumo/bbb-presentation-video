from math import radians
from typing import TypeVar

import cairo

from bbb_presentation_video.events import Size
from bbb_presentation_video.renderer.tldraw.shape import (
    StickyShape,
    apply_shape_rotation,
)
from bbb_presentation_video.renderer.tldraw.shape.text import finalize_sticky_text
from bbb_presentation_video.renderer.tldraw.utils import STICKY_FILLS, ColorStyle

CairoSomeSurface = TypeVar("CairoSomeSurface", bound="cairo.Surface")


def rounded_rect(
    ctx: "cairo.Context[CairoSomeSurface]", size: Size, radius: float
) -> None:
    ctx.new_sub_path()
    ctx.arc(size.width - radius, radius, radius, radians(-90), radians(0))
    ctx.arc(size.width - radius, size.height - radius, radius, radians(0), radians(90))
    ctx.arc(radius, size.height - radius, radius, radians(90), radians(180))
    ctx.arc(radius, radius, radius, radians(180), radians(270))
    ctx.close_path()


def finalize_sticky(ctx: "cairo.Context[CairoSomeSurface]", shape: StickyShape) -> None:
    apply_shape_rotation(ctx, shape)

    style = shape.style
    if style.color is ColorStyle.WHITE or style.color is ColorStyle.BLACK:
        style.color = ColorStyle.YELLOW

    # Shadow. Doing blurred shadow is hard, so this is a simple offset drop shadow + border instead
    ctx.save()
    ctx.translate(-1.0, -1.0)
    blur_size = Size(shape.size.width + 3, shape.size.height + 3)
    rounded_rect(ctx, blur_size, 5)
    ctx.set_source_rgba(0, 0, 0, 0.15)
    ctx.fill()
    ctx.restore()
    rounded_rect(ctx, shape.size, 3)
    ctx.set_source_rgba(0, 0, 0, 0.15)
    ctx.set_line_width(2.0)
    ctx.stroke_preserve()

    # And fill with sticky note background color
    ctx.set_source_rgb(*STICKY_FILLS[style.color])
    ctx.fill()

    finalize_sticky_text(ctx, shape)