# -*- coding: utf-8 -*-
'''
    feedgen.ext.podcast_google
    ~~~~~~~~~~~~~~~~~~~

    Extends the FeedGenerator to produce Googles.

    :copyright: 2023, Lucas Barros <lucas.barros@luizalabs.com>

    :license: FreeBSD and LGPL, see license.* for more details.
'''

from feedgen.compat import string_types
from feedgen.ext.base import BaseExtension
from feedgen.util import ensure_format, xml_elem


class PodcstGoogleExtension(BaseExtension):
    '''FeedGenerator extension for Googles.
    '''

    def __init__(self):
        # Googfleplay tags
        self.__google_author = None
        self.__google_block = None
        self.__google_category = None
        self.__google_image = None
        self.__google_explicit = None
        self.__google_complete = None
        self.__google_new_feed_url = None
        self.__google_owner = None
        self.__google_subtitle = None
        self.__google_summary = None

    def extend_ns(self):
        return {'googleplay': 'http://www.google.com/schemas/play-podcasts/1.0'}

    def extend_rss(self, rss_feed):
        '''Extend an RSS feed root with set google fields.

        :returns: The feed root element.
        '''
        GOOGLE_NS = 'http://www.google.com/schemas/play-podcasts/1.0'
        channel = rss_feed[0]

        if self.__google_author:
            author = xml_elem('{%s}author' % GOOGLE_NS, channel)
            author.text = self.__google_author

        if self.__google_block is not None:
            block = xml_elem('{%s}block' % GOOGLE_NS, channel)
            block.text = 'yes' if self.__google_block else 'no'

        for c in self.__google_category or []:
            if not c.get('cat'):
                continue
            category = channel.find(
                    '{%s}category[@text="%s"]' % (GOOGLE_NS, c.get('cat')))
            if category is None:
                category = xml_elem('{%s}category' % GOOGLE_NS, channel)
                category.attrib['text'] = c.get('cat')

            if c.get('sub'):
                subcategory = xml_elem('{%s}category' % GOOGLE_NS, category)
                subcategory.attrib['text'] = c.get('sub')

        if self.__google_image:
            image = xml_elem('{%s}image' % GOOGLE_NS, channel)
            image.attrib['href'] = self.__google_image

        if self.__google_explicit in ('yes', 'no', 'clean'):
            explicit = xml_elem('{%s}explicit' % GOOGLE_NS, channel)
            explicit.text = self.__google_explicit

        if self.__google_complete in ('yes', 'no'):
            complete = xml_elem('{%s}complete' % GOOGLE_NS, channel)
            complete.text = self.__google_complete

        if self.__google_new_feed_url:
            new_feed_url = xml_elem('{%s}new-feed-url' % GOOGLE_NS, channel)
            new_feed_url.text = self.__google_new_feed_url

        if self.__google_owner:
            owner = xml_elem('{%s}owner' % GOOGLE_NS, channel)
            owner_name = xml_elem('{%s}name' % GOOGLE_NS, owner)
            owner_name.text = self.__google_owner.get('name')
            owner_email = xml_elem('{%s}email' % GOOGLE_NS, owner)
            owner_email.text = self.__google_owner.get('email')

        if self.__google_subtitle:
            subtitle = xml_elem('{%s}subtitle' % GOOGLE_NS, channel)
            subtitle.text = self.__google_subtitle

        if self.__google_summary:
            summary = xml_elem('{%s}summary' % GOOGLE_NS, channel)
            summary.text = self.__google_summary

        return rss_feed

    def google_author(self, google_author=None):
        '''Get or set the googleplay:author. The content of this tag is shown in
        the Artist column in Google. If the tag is not present, Google uses the
        contents of the <author> tag. If <googleplay:author> is not present at the
        feed level, Google will use the contents of <managingEditor>.

        :param google_author: The author of the Google.
        :returns: The author of the Google.
        '''
        if google_author is not None:
            self.__google_author = google_author
        return self.__google_author

    def google_block(self, google_block=None):
        '''Get or set the Google block attribute. Use this to prevent the
        entire Google from appearing in the Google Google directory.

        :param google_block: Block the Google.
        :returns: If the Google is blocked.
        '''
        if google_block is not None:
            self.__google_block = google_block
        return self.__google_block

    def google_category(self, google_category=None, replace=False, **kwargs):
        '''Get or set the Google category which appears in the category column
        and in Google Store Browser.

         
        This method can be called with:

        - the fields of an google_category as keyword arguments
        - the fields of an google_category as a dictionary
        - a list of dictionaries containing the google_category fields

        An google_category has the following fields:

        - *cat* name for a category.
        - *sub* name for a subcategory, child of category

        If a Google has more than one subcategory from the same category, the
        category is called more than once.

        Likei the parameter::

            [{"cat":"Arts","sub":"Design"},{"cat":"Arts","sub":"Food"}]

        

        :param google_category: Dictionary or list of dictionaries with
                                google_category data.
        :param replace: Add or replace old data.
        :returns: List of google_categories as dictionaries.

        ---

        **Important note about deprecated parameter syntax:** Old version of
        the feedgen did only support one category plus one subcategory which
        would be passed to this ducntion as first two parameters. For
        compatibility reasons, this still works but should not be used any may
        be removed at any time.
        '''
        # Ensure old API still works for now. Note that the API is deprecated
        # and this fallback may be removed at any time.
        if isinstance(google_category, string_types):
            google_category = {'cat': google_category}
            if replace:
                google_category['sub'] = replace
            replace = True
        if google_category is None and kwargs:
            google_category = kwargs
        if google_category is not None:
            if replace or self.__google_category is None:
                self.__google_category = []
            self.__google_category += ensure_format(google_category,
                                                    set(['cat', 'sub']),
                                                    set(['cat']))
        return self.__google_category

    def google_image(self, google_image=None):
        '''
        :param google_image: Image of the Google.
        :returns: Image of the Google.
        '''
        if google_image is not None:
            if google_image.endswith('.jpg') or google_image.endswith('.png'):
                self.__google_image = google_image
            else:
                ValueError('Image file must be png or jpg')
        return self.__google_image

    def google_explicit(self, google_explicit=None):
        ''' 
        :param google_explicit: If the Google contains explicit material.
        :returns: If the Google contains explicit material.
        '''
        if google_explicit is not None:
            if google_explicit not in ('', 'yes', 'no', 'clean'):
                raise ValueError('Invalid value for explicit tag')
            self.__google_explicit = google_explicit
        return self.__google_explicit

    def google_complete(self, google_complete=None):
        '''
        :param google_complete: If the Google is complete.
        :returns: If the Google is complete.
        '''
        if google_complete is not None:
            if google_complete not in ('yes', 'no', '', True, False):
                raise ValueError('Invalid value for complete tag')
            if google_complete is True:
                google_complete = 'yes'
            if google_complete is False:
                google_complete = 'no'
            self.__google_complete = google_complete
        return self.__google_complete

    def google_new_feed_url(self, google_new_feed_url=None):
        '''
        :param google_new_feed_url: New feed URL.
        :returns: New feed URL.
        '''
        if google_new_feed_url is not None:
            self.__google_new_feed_url = google_new_feed_url
        return self.__google_new_feed_url

    def google_owner(self, name=None, email=None):
        '''
        :param google_owner: The owner of the feed.
        :returns: Data of the owner of the feed.
        '''
        if name is not None:
            if name and email:
                self.__google_owner = {'name': name, 'email': email}
            elif not name and not email:
                self.__google_owner = None
            else:
                raise ValueError('Both name and email have to be set.')
        return self.__google_owner

    def google_subtitle(self, google_subtitle=None):
        '''
        :param google_subtitle: Subtitle of the Google.
        :returns: Subtitle of the Google.
        '''
        if google_subtitle is not None:
            self.__google_subtitle = google_subtitle
        return self.__google_subtitle

    def google_summary(self, google_summary=None):
        '''
        :param google_summary: Summary of the Google.
        :returns: Summary of the Google.
        '''
        if google_summary is not None:
            self.__google_summary = google_summary
        return self.__google_summary

    _google_categories = {
            'Arts': [
                'Design', 'Fashion & Beauty', 'Food', 'Literature',
                'Performing Arts', 'Visual Arts'],
            'Business': [
                'Business News', 'Careers', 'Investing',
                'Management & Marketing', 'Shopping'],
            'Comedy': [],
            'Education': [
                'Education', 'Education Technology', 'Higher Education',
                'K-12', 'Language Courses', 'Training'],
            'Games & Hobbies': [
                'Automotive', 'Aviation', 'Hobbies', 'Other Games',
                'Video Games'],
            'Government & Organizations': [
                'Local', 'National', 'Non-Profit', 'Regional'],
            'Health': [
                'Alternative Health', 'Fitness & Nutrition', 'Self-Help',
                'Sexuality'],
            'Kids & Family': [],
            'Music': [],
            'News & Politics': [],
            'Religion & Spirituality': [
                'Buddhism', 'Christianity', 'Hinduism', 'Islam', 'Judaism',
                'Other', 'Spirituality'],
            'Science & Medicine': [
                'Medicine', 'Natural Sciences', 'Social Sciences'],
            'Society & Culture': [
                'History', 'Personal Journals', 'Philosophy',
                'Places & Travel'],
            'Sports & Recreation': [
                'Amateur', 'College & High School', 'Outdoor', 'Professional'],
            'Technology': [
                'Gadgets', 'Tech News', 'Googleing', 'Software How-To'],
            'TV & Film': []}
