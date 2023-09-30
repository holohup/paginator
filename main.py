from typing import NamedTuple


class Interval(NamedTuple):
    """A handy class to define intervals."""

    start: int
    end: int


class Paginator:
    """Main paginator class. Use method get_pages() for the pagination str."""

    def __init__(
        self, current_page: int, total_pages: int, boundaries: int, around: int
    ) -> None:
        self._current_page = current_page
        self._total_pages = total_pages
        self._boundaries = boundaries
        self._around = around
        self._validate_values()
        self._mid_interval = self._left_interval = self._right_interval = None

    def get_pages(self) -> str:
        return ' '.join(self._generate_resulting_list())

    def _generate_resulting_list(self) -> list[str]:
        self._find_intervals()
        result = []
        result.extend(generate_ascending_numbers_list(self._left_interval))
        self._append_ellipsis(result, self._left_interval, self._mid_interval)
        result.extend(generate_ascending_numbers_list(self._mid_interval))
        self._append_ellipsis(result, self._mid_interval, self._right_interval)
        result.extend(generate_ascending_numbers_list(self._right_interval))
        return result

    def _find_intervals(self):
        self._mid_interval = Interval(
            max(1, self._current_page - self._around),
            min(self._current_page + self._around, self._total_pages),
        )
        self._left_interval = Interval(
            1, min(self._boundaries, self._mid_interval.start - 1)
        )
        self._right_interval = Interval(
            max(
                self._mid_interval.end + 1,
                self._total_pages - self._boundaries + 1,
            ),
            self._total_pages,
        )

    def _append_ellipsis(
        self, res: list[str], left_interv: Interval, right_interv: Interval
    ) -> str:
        if left_interv.end + 1 >= right_interv.start:
            return
        res.append('...')

    def _validate_values(self):
        if (
            not self._all_values_passed_are_integers
            or not self._all_values_non_negative
            or self._current_page > self._total_pages
        ):
            raise ValueError('Invalid pagination parameters values.')

    @property
    def _all_values_non_negative(self) -> bool:
        return all((attr >= 0 for attr in self._attrs_to_validate))

    @property
    def _all_values_passed_are_integers(self) -> bool:
        return all(isinstance(attr, int) for attr in self._attrs_to_validate)

    @property
    def _attrs_to_validate(self):
        return (getattr(self, val) for val in (
            '_current_page',
            '_total_pages',
            '_boundaries',
            '_around',
        ))


def generate_ascending_numbers_list(interval: Interval) -> list[str]:
    """Returns a list of ascending integer strings.
    From start to finish inclusive."""

    return list(map(str, range(interval.start, interval.end + 1)))
