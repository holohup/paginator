from typing import NamedTuple


class Interval(NamedTuple):
    """A handy tuple to define intervals."""

    start: int
    end: int


class Paginator:
    """Main paginator class. Use method get_pages() for the pagination str."""

    OPEN, CLOSE = -1, 1
    _attrs = '_current_page', '_last_page', '_boundaries', '_around'

    def __init__(
        self, current_page: int, total_pages: int, boundaries: int, around: int
    ) -> None:
        self._current_page = current_page
        self._last_page = total_pages
        self._first_page = 1
        self._boundaries = boundaries
        self._around = around
        self._validate_values()

    def print_pagination(self) -> None:
        print(self.get_pages())

    def get_pages(self) -> str:
        sorted_events = sorted(self._scribe_interval_events())
        sorted_intervals = self._sort_open_intervals(sorted_events)
        return ' '.join(self._generate_pagination_results(sorted_intervals))

    def _scribe_interval_events(self) -> list[tuple]:
        events = [
            (
                max(self._first_page, self._current_page - self._around),
                self.OPEN,
            ),
            (
                min(self._current_page + self._around, self._last_page),
                self.CLOSE,
            ),
        ]
        if self._boundaries > 0:
            self._add_boundaries_events(events)
        return events

    def _add_boundaries_events(self, events: list[tuple]) -> None:
        boundaries_events = [
            (self._first_page, self.OPEN),
            (min(self._boundaries, self._last_page), self.CLOSE),
            (
                max(self._first_page, self._last_page - self._boundaries + 1),
                self.OPEN,
            ),
            (self._last_page, self.CLOSE),
        ]
        events.extend(boundaries_events)

    def _sort_open_intervals(self, intervals: list[tuple]) -> list[Interval]:
        open_intervals = []
        open_intervals_sum = 0
        interval_start = None
        for interval in intervals:
            if interval[1] == self.OPEN:
                open_intervals_sum += 1
            elif interval[1] == self.CLOSE:
                open_intervals_sum -= 1
            if open_intervals_sum > 0 and interval_start is None:
                interval_start = interval[0]
            if open_intervals_sum <= 0 and interval_start is not None:
                open_intervals.append(Interval(interval_start, interval[0]))
                interval_start = None
        return open_intervals

    def _generate_pagination_results(self, intervals: list[Interval]):
        last_end = 0
        for i in intervals:
            if i.start - last_end > 1:
                yield '...'
            yield ' '.join(map(str, range(i.start, i.end + 1)))
            last_end = i.end
        if last_end < self._last_page:
            yield '...'

    def _validate_values(self) -> None:
        if self._negative_attr_present or self._current_page > self._last_page:
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
    p = Paginator(50_000_000, 100_000_000, 3, 2)
    p.print_pagination()
