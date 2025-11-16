from fastapi import APIRouter
from fastapi.responses import HTMLResponse

import htpy as h

from backend.routes.react import EntryPoint, entrypoint_path


ui_router = APIRouter()


@ui_router.get("/")
async def hello():
    return HTMLResponse(
        h.html[
            h.head[
                h.meta(charset="utf-8"),
                h.title["TODO"],
                h.link(href="/styles.css", rel="stylesheet"),
            ],
            h.body[
                h.h1(class_="text-3xl font-bold underline")[
                    " Hello From Scrum Master! "
                ],
                h.ul[
                    h.li[h.a(href="/react")["React endpoint"]],
                    h.li[h.a(href="/ssr")["SSR endpoint"]],
                ],
            ],
        ]
    )


@ui_router.get("/react")
async def react():
    return HTMLResponse(
        h.html[
            h.head[
                h.meta(charset="utf-8"),
                h.title["TODO"],
                h.link(href="/styles.css", rel="stylesheet"),
            ],
            h.body[
                h.h1(class_="text-3xl font-bold underline")[" Hello From REACT! "],
                h.a(href="/")["Home"],
                h.div(id="root"),
                h.script(type="module", src=entrypoint_path(EntryPoint.TEST_ENTRY)),
            ],
        ]
    )


@ui_router.get("/ssr")
async def ssr():
    return HTMLResponse(
        h.html[
            h.head[
                h.meta(charset="utf-8"),
                h.title["TODO"],
                h.link(href="/styles.css", rel="stylesheet"),
            ],
            h.h1(class_="text-3xl font-bold underline")["Hello From SSR!"],
            h.a(href="/")["Home"],
        ]
    )
