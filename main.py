from typing import NamedTuple


class Interval(NamedTuple):
    """A handy tuple to define intervals."""

    start: int
    end: int


class Paginator:
    """Main paginator class. Use method get_pages() for the pagination str."""

    _open, _close = -1, 1
    _attrs = '_current_page', '_total_pages', '_boundaries', '_around'

    def __init__(
        self, current_page: int, total_pages: int, boundaries: int, around: int
    ) -> None:
        self._current_page = current_page
        self._total_pages = total_pages
        self._boundaries = boundaries
        self._around = around
        self._validate_values()

    def print_pagination(self) -> None:
        print(self.get_pages())

    def get_pages(self) -> str:
        sorted_events = sorted(self._scribe_interval_events())
        sorted_intervals = self._sort_open_intervals(sorted_events)
        return ' '.join(self._pagination_results_generator(sorted_intervals))

    def _scribe_interval_events(self) -> list[tuple]:
        events = [
            (max(1, self._current_page - self._around), self._open),
            (
                min(self._current_page + self._around, self._total_pages),
                self._close,
            ),
        ]
        if self._boundaries > 0:
            self._add_boundaries_events(events)
        return events

    def _add_boundaries_events(self, events: list[tuple]) -> None:
        events.extend(
            [
                (1, self._open),
                (min(self._boundaries, self._total_pages), self._close),
                (max(1, self._total_pages - self._boundaries + 1), self._open),
                (self._total_pages, self._close),
            ]
        )

    def _sort_open_intervals(self, intervals: list[tuple]) -> list[Interval]:
        open_intervals = [Interval(0, 0)]
        open_intervals_sum = 0
        interval_start = None
        for interval in intervals:
            if interval[1] == self._open:
                open_intervals_sum += 1
            elif interval[1] == self._close:
                open_intervals_sum -= 1
            if open_intervals_sum > 0 and interval_start is None:
                interval_start = interval[0]
            if open_intervals_sum <= 0 and interval_start is not None:
                open_intervals.append(Interval(interval_start, interval[0]))
                interval_start = None
        return open_intervals

    def _pagination_results_generator(self, intervals: list[Interval]):
        for i in range(1, len(intervals)):
            if intervals[i].start - intervals[i - 1].end > 1:
                yield '...'
            yield ' '.join(
                map(str, range(intervals[i].start, intervals[i].end + 1))
            )
        if intervals[-1].end < self._total_pages:
            yield '...'

    def _validate_values(self) -> None:
        if (
            self._negative_attr_present
            or self._current_page > self._total_pages
        ):
            raise ValueError('Invalid pagination parameters values.')
        if not self._all_attrs_are_integers:
            raise TypeError('Pagination requires all integer numbers.')

    @property
    def _negative_attr_present(self) -> bool:
        return any((getattr(self, a) < 0 for a in self._attrs))

    @property
    def _all_attrs_are_integers(self) -> bool:
        return all(isinstance(getattr(self, a), int) for a in self._attrs)


if __name__ == '__main__':
    p = Paginator(50_000_000, 100_000_000, 10, 3)
    p.print_pagination()
