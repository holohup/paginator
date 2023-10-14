from typing import NamedTuple


class Interval(NamedTuple):
    """A handy tuple to define intervals."""

    start: int
    end: int


class Paginator:
    """Main paginator class. Use method get_pages() for the pagination str."""

    OPEN, CLOSE = -1, 1
    _FIRST_PAGE = 1

    def __init__(
        self, current_page: int, total_pages: int, boundaries: int, around: int
    ) -> None:
        self._validate_values(current_page, total_pages, boundaries, around)
        self._current_page = current_page
        self._last_page = total_pages
        self._boundaries = boundaries
        self._around = around

    def print_pagination(self) -> None:
        print(self.get_pages())

    def get_pages(self) -> str:
        sorted_events = sorted(self._scribe_interval_events())
        sorted_intervals = self._sort_open_intervals(sorted_events)
        return ' '.join(self._generate_pagination_results(sorted_intervals))

    def _scribe_interval_events(self) -> list[tuple]:
        events = [
            (
                max(self._FIRST_PAGE, self._current_page - self._around),
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
            (self._FIRST_PAGE, self.OPEN),
            (min(self._boundaries, self._last_page), self.CLOSE),
            (
                max(self._FIRST_PAGE, self._last_page - self._boundaries + 1),
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
            open_intervals_sum -= interval[1]
            if open_intervals_sum > 0 and interval_start is None:
                interval_start = interval[0]
            if open_intervals_sum <= 0 and interval_start is not None:
                open_intervals.append(Interval(interval_start, interval[0]))
                interval_start = None
        return open_intervals

    def _generate_pagination_results(self, intervals: list[Interval]):
        last_end = 0
        for interval in intervals:
            if interval.start - last_end > 1:
                yield '...'
            yield ' '.join(map(str, range(interval.start, interval.end + 1)))
            last_end = interval.end
        if last_end < self._last_page:
            yield '...'

    @staticmethod
    def _validate_values(
        current_page: int, total_pages: int, boundaries: int, around: int
    ) -> None:
        if not all(
            [
                type(value) is int
                for value in (current_page, total_pages, boundaries, around)
            ]
        ):
            raise TypeError('Pagination requires all integers.')

        if any(
            (current_page < 0, total_pages < 0, boundaries < 0, around < 0)
        ):
            raise ValueError(
                'Pagination parameters cannot be negative values.'
            )

        if current_page > total_pages:
            raise ValueError('Current page cannot be bigger then total pages.')


if __name__ == '__main__':
    p = Paginator(50_000_000, 100_000_000, 3, 2)
    p.print_pagination()
