"""Format matrices for printing and display."""
from typing import TypedDict, Sequence, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from . import MatrixABC


class FormatParameters(TypedDict):
    """Typed Dictionary Type for Matrix formatting parameters."""
    frame_top_left_corner: str
    frame_top_bar: str
    frame_top_junction: str
    frame_top_right_corner: str
    frame_left_bar: str
    frame_left_junction: str
    frame_right_bar: str
    frame_right_junction: str
    frame_bottom_left_corner: str
    frame_bottom_right_corner: str
    frame_bottom_bar: str
    frame_bottom_junction: str
    headrow_cell_pre: str
    headrow_cell_post: str
    headrow_top_left_corner: str
    headrow_top_bar: str
    headrow_top_headcol_junction: str
    headrow_headcol_bar: str
    headrow_top_junction: str
    headrow_top_right_corner: str
    headrow_left_bar: str
    headrow_right_bar: str
    headrow_bottom_bar: str
    headrow_bottom_junction: str
    headrow_bottom_right_corner: str
    headrow_hdiv_bar: str
    headcol_cell_pre: str
    headcol_cell_post: str
    headcol_top_left_corner: str
    headcol_top_bar: str
    headcol_top_right_corner: str
    headcol_left_bar: str
    headcol_left_junction: str
    headcol_bottom_left_corner: str
    headcol_bottom_bar: str
    headcol_bottom_right_corner: str
    headcol_vdiv_bar: str
    bottom_right_corner: str
    bottom_junction: str
    bottom_bar: str
    left_junction: str
    left_bar: str
    right_junction: str
    right_bar: str
    hdiv_bar: str
    vdiv_bar: str
    mid_junction: str
    cell_pre: str
    cell_post: str


class Formatter:

    fmt: FormatParameters

    def __init__(self, fmt: FormatParameters):
        self.fmt = fmt

    def __call__(
            self,
            m: "MatrixABC[Any]",
            colheaders: Sequence[str] | None = None,
            rowheaders: Sequence[str] | None = None,
            cornerhead: str | None = None
    ) -> str:
        if m.shape[0] == 0 or m.shape[1] == 0:
            # Special case: 0x0 matrix
            return "[ ]"  # @TODO: Improve empty fmt
        rowrange = range(0, m.shape[0])
        colrange = range(0, m.shape[1])
        cornerhead = "" if cornerhead is None else str(cornerhead)
        data = self._prepare_data(m, colrange, rowrange)
        colheaders = self._prepare_headers(colheaders, colrange)
        rowheaders = self._prepare_headers(rowheaders, rowrange)
        colheaders = self._preformat_colheaders(colheaders, colrange)
        rowheaders = self._preformat_rowheaders(rowheaders, rowrange)
        data = self._preformat_cells(data, colrange, rowrange)
        data, colheaders, rowheaders, cornerhead = self._align_columns(
            data, colheaders, rowheaders, cornerhead, colrange, rowrange
        )
        return self._build_string(data, colheaders, rowheaders, cornerhead, colrange, rowrange).strip("\n")

    def _prepare_data(
            self,
            m: "MatrixABC[Any]",
            colrange: range,
            rowrange: range
            ) -> list[list[str]]:
        """Transpose and stringify matrix data.

        Takes a sequence of sequences of the shape [row, row, ...] and type Any,
        and turns it into a list of lists of the shape [col, col, ...]."""
        data = m.aslist()
        cols: list[list[str]] = []
        for col in colrange:
            col_values: list[str] = []
            for row in rowrange:
                col_values.append(str(data[row][col]))
            cols.append(col_values)
        return cols

    def _prepare_headers(
            self,
            headers: Sequence[Any] | None,
            headerrange: range
            ) -> list[str]:
        """Stringify and extend headers if needed.

        Makes sure missing headers are filled in with numeric descriptors and
        all labels are strings."""
        if isinstance(headers, Sequence):
            processed_headers: list[str] = []
            length = len(headers)
            for col in headerrange:
                processed_headers.append(
                    str(headers[col]) if col < length else str(col)
                )
        else:
            processed_headers = [str(col) for col in headerrange]
        return processed_headers

    def _preformat_colheaders(
            self,
            colheaders: list[str],
            colrange: range
            ) -> list[str]:
        """Preformat colheader cells by adding any pre- and post-datum formatting."""
        for col in colrange:
            colheaders[col] = "".join((
                self.fmt["headrow_cell_pre"],
                colheaders[col],
                self.fmt["headrow_cell_post"]
            ))
        return colheaders

    def _preformat_rowheaders(
            self,
            rowheaders: list[str],
            rowrange: range
            ) -> list[str]:
        """Preformat rowheader cells by adding any pre- and post-datum formatting."""
        for row in rowrange:
            rowheaders[row] = "".join((
                self.fmt["headcol_cell_pre"],
                rowheaders[row],
                self.fmt["headcol_cell_post"]
            ))
        return rowheaders

    def _preformat_cells(
            self,
            data: list[list[str]],
            colrange: range,
            rowrange: range
            ) -> list[list[str]]:
        """Preformat cells by adding any pre- and post-datum formatting."""
        for col in colrange:
            for row in rowrange:
                data[col][row] = "".join((
                    self.fmt["cell_pre"],
                    data[col][row],
                    self.fmt["cell_post"]
                ))
        return data

    def _align_columns(
            self,
            data: list[list[str]],
            colheaders: list[str],
            rowheaders: list[str],
            cornerhead: str,
            colrange: range,
            rowrange: range
            ) -> tuple[list[list[str]], list[str], list[str], str]:
        """Align cell content in each column with spaces to be the same width."""
        # Compute regular columns
        for col in colrange:
            max_width = len(max(data[col], key=len))
            if len(colheaders[col]) > max_width:
                max_width = len(colheaders[col])
            colheaders[col] = colheaders[col].rjust(max_width)
            for row in rowrange:
                data[col][row] = data[col][row].rjust(max_width)
        # Compute row header column
        max_width = len(max(rowheaders, key=len))
        if len(cornerhead) > max_width:
            max_width = len(cornerhead)
        cornerhead = cornerhead.rjust(max_width)
        for row in rowrange:
            rowheaders[row] = rowheaders[row].rjust(max_width)
        return (data, colheaders, rowheaders, cornerhead)

    def _build_string(    # noqa: C901
            self,
            data: list[list[str]],
            colheaders: list[str],
            rowheaders: list[str],
            cornerhead: str,
            colrange: range,
            rowrange: range
            ) -> str:
        rep: list[str] = []
        collimit = max(colrange or [0])
        rowlimit = max(rowrange or [0])

        # Frame-Top
        rep.append(self.fmt["frame_top_left_corner"])
        rep.append(self.fmt["frame_top_bar"] * len(cornerhead))
        rep.append(self.fmt["frame_top_bar"] * len(self.fmt["headrow_left_bar"]))
        rep.append(self.fmt["frame_top_junction"])
        for col in colrange:
            rep.append(self.fmt["frame_top_bar"] * len(colheaders[col]))
            if col < collimit:
                rep.append(self.fmt["frame_top_junction"])
            else:
                rep.append(self.fmt["frame_top_bar"] * len(self.fmt["headrow_right_bar"]))
                rep.append(self.fmt["frame_top_right_corner"])

        # Headrow-Top
        rep.append(self.fmt["frame_left_bar"])
        rep.append(self.fmt["headrow_top_left_corner"])
        rep.append(self.fmt["headrow_top_bar"] * len(cornerhead))
        rep.append(self.fmt["headrow_top_headcol_junction"])
        for col in colrange:
            rep.append(self.fmt["headrow_top_bar"] * len(colheaders[col]))
            rep.append(self.fmt["headrow_top_junction"] if col < collimit else self.fmt["headrow_top_right_corner"])
        rep.append(self.fmt["frame_right_bar"])

        # Headrow-Cells
        rep.append(self.fmt["frame_left_bar"])
        rep.append(self.fmt["headrow_left_bar"])
        rep.append(cornerhead)
        rep.append(self.fmt["headrow_headcol_bar"])
        for col in colrange:
            rep.append(colheaders[col])
            rep.append(self.fmt["headrow_hdiv_bar"] if col < collimit else self.fmt["headrow_right_bar"])
        rep.append(self.fmt["frame_right_bar"])

        # Headrow-Bottom
        rep.append(self.fmt["frame_left_junction"])
        rep.append(self.fmt["headcol_top_left_corner"])
        rep.append(self.fmt["headcol_top_bar"] * len(cornerhead))
        rep.append(self.fmt["headcol_top_right_corner"])
        for col in colrange:
            rep.append(self.fmt["headrow_bottom_bar"] * len(colheaders[col]))
            rep.append(self.fmt["headrow_bottom_junction"] if col < collimit else self.fmt["headrow_bottom_right_corner"])
        rep.append(self.fmt["frame_right_bar"])

        for row in rowrange:
            # (Normal) Row-Cells
            rep.append(self.fmt["frame_left_bar"])
            rep.append(self.fmt["headcol_left_bar"])
            rep.append(rowheaders[row])
            rep.append(self.fmt["left_bar"])
            for col in colrange:
                rep.append(data[col][row])
                rep.append(self.fmt["hdiv_bar"] if col < collimit else self.fmt["right_bar"])
            rep.append(self.fmt["frame_right_bar"])

            if row < rowlimit:
                # (Normal) Row-Bottom
                rep.append(self.fmt["frame_left_junction"])
                rep.append(self.fmt["headcol_left_junction"])
                rep.append(self.fmt["headcol_vdiv_bar"] * len(cornerhead))
                rep.append(self.fmt["left_junction"])
                for col in colrange:
                    rep.append(self.fmt["vdiv_bar"] * len(colheaders[col]))
                    rep.append(self.fmt["mid_junction"] if col < collimit else self.fmt["right_junction"])
                rep.append(self.fmt["frame_right_junction"])

            else:
                # (Final) Row-Bottom
                rep.append(self.fmt["frame_left_junction"])
                rep.append(self.fmt["headcol_bottom_left_corner"])
                rep.append(self.fmt["headcol_bottom_bar"] * len(cornerhead))
                rep.append(self.fmt["headcol_bottom_right_corner"])
                for col in colrange:
                    rep.append(self.fmt["bottom_bar"] * len(colheaders[col]))
                    rep.append(self.fmt["bottom_junction"] if col < collimit else self.fmt["bottom_right_corner"])
                rep.append(self.fmt["frame_right_junction"])

        # Frame-Bottom
        rep.append(self.fmt["frame_bottom_left_corner"])
        rep.append(self.fmt["frame_bottom_bar"] * len(cornerhead))
        rep.append(self.fmt["frame_bottom_bar"] * len(self.fmt["headrow_left_bar"]))
        rep.append(self.fmt["frame_bottom_junction"])
        for col in colrange:
            rep.append(self.fmt["frame_bottom_bar"] * len(colheaders[col]))
            if col < collimit:
                rep.append(self.fmt["frame_bottom_junction"])
            else:
                rep.append(self.fmt["frame_bottom_bar"] * len(self.fmt["headrow_right_bar"]))
                rep.append(self.fmt["frame_bottom_right_corner"])

        return "".join(rep)


PlainFormatter = Formatter({
    "frame_top_left_corner":        "",
    "frame_top_bar":                "",
    "frame_top_junction":           "",
    "frame_top_right_corner":       "",
    "frame_left_bar":               "",
    "frame_left_junction":          "",
    "frame_right_bar":              "",
    "frame_right_junction":         "\n",
    "frame_bottom_left_corner":     "",
    "frame_bottom_right_corner":    "",
    "frame_bottom_bar":             "",
    "frame_bottom_junction":        "",
    "headrow_cell_pre":             " ",
    "headrow_cell_post":            " ",
    "headrow_top_left_corner":      "",
    "headrow_top_bar":              "",
    "headrow_top_headcol_junction": "",
    "headrow_headcol_bar":          "",
    "headrow_top_junction":         "",
    "headrow_top_right_corner":     "",
    "headrow_left_bar":             "",
    "headrow_right_bar":            "\n",
    "headrow_bottom_bar":           "",
    "headrow_bottom_junction":      "",
    "headrow_bottom_right_corner":  "",
    "headrow_hdiv_bar":             "",
    "headcol_cell_pre":             " ",
    "headcol_cell_post":            " ",
    "headcol_top_left_corner":      "",
    "headcol_top_bar":              "",
    "headcol_top_right_corner":     "",
    "headcol_left_bar":             "",
    "headcol_left_junction":        "",
    "headcol_bottom_left_corner":   "",
    "headcol_bottom_bar":           "",
    "headcol_bottom_right_corner":  "",
    "headcol_vdiv_bar":             "",
    "bottom_right_corner":          "",
    "bottom_junction":              "",
    "bottom_bar":                   "",
    "left_junction":                "",
    "left_bar":                     "",
    "right_junction":               "",
    "right_bar":                    "",
    "hdiv_bar":                     "",
    "vdiv_bar":                     "",
    "mid_junction":                 "",
    "cell_pre":                     " ",
    "cell_post":                    " "
})

SimpleFormatter = Formatter({
    "frame_top_left_corner":        "",
    "frame_top_bar":                "",
    "frame_top_junction":           "",
    "frame_top_right_corner":       "",
    "frame_left_bar":               "",
    "frame_left_junction":          "",
    "frame_right_bar":              "\n",
    "frame_right_junction":         "\n",
    "frame_bottom_left_corner":     "",
    "frame_bottom_right_corner":    "",
    "frame_bottom_bar":             "",
    "frame_bottom_junction":        "",
    "headrow_cell_pre":             " ",
    "headrow_cell_post":            " ",
    "headrow_top_left_corner":      "+",
    "headrow_top_bar":              "-",
    "headrow_top_headcol_junction": "-+",
    "headrow_headcol_bar":          " |",
    "headrow_top_junction":         "+",
    "headrow_top_right_corner":     "+",
    "headrow_left_bar":             "|",
    "headrow_right_bar":            "|",
    "headrow_bottom_bar":           "=",
    "headrow_bottom_junction":      "+",
    "headrow_bottom_right_corner":  "+",
    "headrow_hdiv_bar":             "|",
    "headcol_cell_pre":             " ",
    "headcol_cell_post":            " ",
    "headcol_top_left_corner":      "+",
    "headcol_top_bar":              "-",
    "headcol_top_right_corner":     "++",
    "headcol_left_bar":             "|",
    "headcol_left_junction":        "+",
    "headcol_bottom_left_corner":   "+",
    "headcol_bottom_bar":           "-",
    "headcol_bottom_right_corner":  "++",
    "headcol_vdiv_bar":             "-",
    "bottom_right_corner":          "+",
    "bottom_junction":              "+",
    "bottom_bar":                   "-",
    "left_junction":                "++",
    "left_bar":                     "||",
    "right_junction":               "+",
    "right_bar":                    "|",
    "hdiv_bar":                     "|",
    "vdiv_bar":                     "-",
    "mid_junction":                 "+",
    "cell_pre":                     " ",
    "cell_post":                    " "
})

FancyFormatter = Formatter({
    "frame_top_left_corner":        "",
    "frame_top_bar":                "",
    "frame_top_junction":           "",
    "frame_top_right_corner":       "",
    "frame_left_bar":               "",
    "frame_left_junction":          "",
    "frame_right_bar":              "\n",
    "frame_right_junction":         "\n",
    "frame_bottom_left_corner":     "",
    "frame_bottom_right_corner":    "",
    "frame_bottom_bar":             "",
    "frame_bottom_junction":        "",
    "headrow_cell_pre":             " ",
    "headrow_cell_post":            " ",
    "headrow_top_left_corner":      "╔",
    "headrow_top_bar":              "═",
    "headrow_top_headcol_junction": "╦",
    "headrow_headcol_bar":          "║",
    "headrow_top_junction":         "╦",
    "headrow_top_right_corner":     "╗",
    "headrow_left_bar":             "║",
    "headrow_right_bar":            "║",
    "headrow_bottom_bar":           "═",
    "headrow_bottom_junction":      "╬",
    "headrow_bottom_right_corner":  "╣",
    "headrow_hdiv_bar":             "║",
    "headcol_cell_pre":             " ",
    "headcol_cell_post":            " ",
    "headcol_top_left_corner":      "╠",
    "headcol_top_bar":              "═",
    "headcol_top_right_corner":     "╬",
    "headcol_left_bar":             "║",
    "headcol_left_junction":        "╠",
    "headcol_bottom_left_corner":   "╚",
    "headcol_bottom_bar":           "═",
    "headcol_bottom_right_corner":  "╩",
    "headcol_vdiv_bar":             "═",
    "bottom_right_corner":          "╝",
    "bottom_junction":              "╩",
    "bottom_bar":                   "═",
    "left_junction":                "╬",
    "left_bar":                     "║",
    "right_junction":               "╣",
    "right_bar":                    "║",
    "hdiv_bar":                     "│",
    "vdiv_bar":                     "─",
    "mid_junction":                 "┼",
    "cell_pre":                     " ",
    "cell_post":                    " "
})

MatrixFormatter = Formatter({
    "frame_top_left_corner":        "",
    "frame_top_bar":                "",
    "frame_top_junction":           "",
    "frame_top_right_corner":       "",
    "frame_left_bar":               "",
    "frame_left_junction":          "",
    "frame_right_bar":              "\n",
    "frame_right_junction":         "",
    "frame_bottom_left_corner":     "",
    "frame_bottom_right_corner":    "",
    "frame_bottom_bar":             "",
    "frame_bottom_junction":        "",
    "headrow_cell_pre":             " ",
    "headrow_cell_post":            " ",
    "headrow_top_left_corner":      "",
    "headrow_top_bar":              "",
    "headrow_top_headcol_junction": "",
    "headrow_headcol_bar":          "",
    "headrow_top_junction":         "",
    "headrow_top_right_corner":     "",
    "headrow_left_bar":             " ",
    "headrow_right_bar":            "",
    "headrow_bottom_bar":           " ",
    "headrow_bottom_junction":      "",
    "headrow_bottom_right_corner":  "┐",
    "headrow_hdiv_bar":             "",
    "headcol_cell_pre":             " ",
    "headcol_cell_post":            " ",
    "headcol_top_left_corner":      "",
    "headcol_top_bar":              " ",
    "headcol_top_right_corner":     "┌",
    "headcol_left_bar":             "",
    "headcol_left_junction":        "",
    "headcol_bottom_left_corner":   "",
    "headcol_bottom_bar":           " ",
    "headcol_bottom_right_corner":  "└",
    "headcol_vdiv_bar":             "",
    "bottom_right_corner":          "┘",
    "bottom_junction":              "",
    "bottom_bar":                   " ",
    "left_junction":                "",
    "left_bar":                     "│",
    "right_junction":               "",
    "right_bar":                    "│",
    "hdiv_bar":                     "",
    "vdiv_bar":                     "",
    "mid_junction":                 "",
    "cell_pre":                     " ",
    "cell_post":                    " "
})

HTMLFormatter = Formatter({
    "frame_top_left_corner":        "<table>\n",
    "frame_top_bar":                "",
    "frame_top_junction":           "",
    "frame_top_right_corner":       "",
    "frame_left_bar":               "",
    "frame_left_junction":          "",
    "frame_right_bar":              "\n",
    "frame_right_junction":         "",
    "frame_bottom_left_corner":     "",
    "frame_bottom_right_corner":    "\n</table>",
    "frame_bottom_bar":             "",
    "frame_bottom_junction":        "",
    "headrow_cell_pre":             '<th scope="row">',
    "headrow_cell_post":            "</th>",
    "headrow_top_left_corner":      "\t<thead>\n\t\t<tr>",
    "headrow_top_bar":              "",
    "headrow_top_headcol_junction": "",
    "headrow_headcol_bar":          "\t\t<th></th> ",
    "headrow_top_junction":         "",
    "headrow_top_right_corner":     "",
    "headrow_left_bar":             "",
    "headrow_right_bar":            "",
    "headrow_bottom_bar":           "",
    "headrow_bottom_junction":      "",
    "headrow_bottom_right_corner":  "",
    "headrow_hdiv_bar":             " ",
    "headcol_cell_pre":             '<th scope="col">',
    "headcol_cell_post":            "</th>",
    "headcol_top_left_corner":      "\t\t</tr>\n\t</thead>\n",
    "headcol_top_bar":              "",
    "headcol_top_right_corner":     "\t<tbody>",
    "headcol_left_bar":             "\t\t<tr>\n\t\t\t",
    "headcol_left_junction":        "",
    "headcol_bottom_left_corner":   "",
    "headcol_bottom_bar":           "",
    "headcol_bottom_right_corner":  "",
    "headcol_vdiv_bar":             "",
    "bottom_right_corner":          "\t</tbody>",
    "bottom_junction":              "",
    "bottom_bar":                   "",
    "left_junction":                "",
    "left_bar":                     "",
    "right_junction":               "",
    "right_bar":                    "\n\t\t</tr>",
    "hdiv_bar":                     "",
    "vdiv_bar":                     "",
    "mid_junction":                 "",
    "cell_pre":                     "<td>",
    "cell_post":                    "</td>"
})

DefaultFormatter = MatrixFormatter
