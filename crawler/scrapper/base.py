from datetime import date
from typing import Iterable, List, Tuple

import bs4
from bs4 import BeautifulSoup

# TODO: change to .utils (relative) when converting to package
from utils import get_url, iter_daterange

# typeinfo
Url = str
ArticleLink = Tuple[str, Url]
DateRange = Tuple[date, date]
ArticleLinkGenerator = Iterable[ArticleLink]


class BaseScrapper:
    def __init__(self, name: str):
        pass

    def __repr__(self) -> str:
        return f"<Scrapper[{self.name}]>"


class ITScrapper(BaseScrapper):
    base_archive_url = "https://timesofindia.indiatimes.com/archive"
    offset_1_jan_2020 = 43831

    def __init__(self):
        super().__init__("IndiaTimes")

    @staticmethod
    def _bs4_archive_articles_table(tag: bs4.element.Tag) -> bool:
        """
        Find table which contains articles in articles list page
        """
        t_attrs = {
            "cellpadding": "0",
            "cellspacing": "0",
            "border": "0",
            "width": "100%",
        }
        trs = tag.find_all("tr")
        attrs_chk = tag.attrs == t_attrs
        return attrs_chk and len(trs) > 3 and trs[1].td and trs[1].td.span

    def _get_articles_link_for_a_day(self, archive_url: Url) -> ArticleLinkGenerator:
        """
        Gets all the articles title and link from archive_url for particluar day.

        Parameters
        ----------
        archive_url: str
            URL of articles lists of a particluar day
            (like https://timesofindia.indiatimes.com/2020/9/2/archivelist/year-2020..)

        Return
        ------
        generator object that will yield tuples like (article title, article url)
        """
        html = get_url(archive_url)
        soup = BeautifulSoup(html, "lxml")
        table = soup.find(self._bs4_archive_articles_table)
        assert table

        for span in table.find_all("span"):
            for a in span.find_all("a"):
                yield (a.text, a["href"])

    def _get_article_content(self, article_url: Url) -> str:
        """
        Extract the news content from article
        """
        # TODO: implementaion
        raise NotImplementedError

    def process_article(self):
        raise NotImplementedError

    def get_articles_link(self, date_range: DateRange) -> List[ArticleLinkGenerator]:
        """
        Get the articles link generators for given date range.

        Parameters
        ----------
        date_range: tuple(start date, end date)
            daterange

        Return
        ------
        List of generator objects for articles for each day in daterange at respective
        index

        Example
        -------
        >>> gens = get_articles_link((date(2020, 9, 1), date(2020, 9, 3)))
        >>> print(gens)
        [<generator object ITScrapper._get_articles_link_for_a_day at 0x7f2940e577b0>,
        <generator object ITScrapper._get_articles_link_for_a_day at 0x7f2940e57820>,
        <generator object ITScrapper._get_articles_link_for_a_day at 0x7f2940e57890>]

        >>> for article_gen in gens:
        ...     for article_link in article_gen:
        ...         print(article_link)
        ('Admitted for brain clot ....', 'http://timesofindia.indiatime ....')
        ('Focus on parcels, carg ....', 'http://timesofindia.indiatimes ....')
        ......
        ('Unlock 4.0: APSRTC hopes ....', 'http://timesofindia.indiatimes ....')

        Note
        ----
        We are using generators extensively because using list will lead to creation of
        unnecessary large temp lists which will require more memory to prevent that we
        are lazy processing articles.

        """
        article_gens = []
        for d in iter_daterange(date_range[0], date_range[1]):
            # calculate starttime value
            # formula starttime value on 01/01/2020 + number of days passed from
            # 01/01/2020
            delta = self.offset_1_jan_2020 + (d - date(2020, 1, 1)).days
            archive_url = (
                f"https://timesofindia.indiatimes.com/"
                f"{d.year}/{d.month}/{d.day}/archivelist/"
                f"year-{d.year},month-{d.month},starttime-{delta}.cms"
            )
            article_gens.append(self._get_articles_link_for_a_day(archive_url))
        return article_gens


if __name__ == "__main__":
    srp = ITScrapper()
    # from pprint import pprint as print

    # links = set(
    #    srp._get_articles_link(
    #        "https://timesofindia.indiatimes.com/2020/9/1/archivelist/year-2020,month-9,starttime-44075.cms"
    #    )
    # )
    # redu_links = list(
    #    srp._get_articles_link(
    #        "https://timesofindia.indiatimes.com/2020/9/1/archivelist/year-2020,month-9,starttime-44075.cms"
    #    )
    # )
    # print(len(links))
    # print(len(redu_links))
    # print(links)
