import os
import csv
import string
import codecs

from quest.framework.utilities import get_snake_case
from quest.framework.singleton import Singleton
from quest.engine import core
from quest.engine.vfs import get_matching_files
from quest.engine.prc import get_prc_string, get_prc_bool

def utf_8_encoder(unicode_csv_data: object):
    """
    """

    for line in unicode_csv_data:
        yield line.encode('utf-8')

def unicode_csv_reader(unicode_csv_data: object, dialect: object = csv.excel, **kwargs):
    """
    """

    csv_reader = csv.reader(unicode_csv_data, dialect=dialect, **kwargs)
    for row in csv_reader:
        yield [ cell for cell in row ]

class ApplicationLocalizer(Singleton, core.QuestObject):
    """
    """

    @staticmethod
    def get_backup_text():
        """
        """

        return ''

    def __init__(self, path: str = 'localization'):
        Singleton.__init__(self)
        core.QuestObject.__init__(self)
        self.__active_language = None
        self.__encoding = get_prc_string('pq-loc-encoding', 'utf-8')
        self.__delimiter = get_prc_string('pq-loc-delimiter', ',')
        self.__warnings = get_prc_bool('pq-loc-warnings', True)
        self.__resources = {}
        self.__load_all_files(path)

    def __load_all_files(self, root: str) -> None:
        """
        """

        self.notify.info('Reading localization files from: %s' % root)
        files = get_matching_files(root, '*.csv')
        if not len(files):
            self.notify.warning('Failed to setup localization. No files found')

        for csv_file in files:
            name = os.path.splitext(os.path.basename(csv_file))[0]
            self.notify.debug('Reading localization file: %s' % name)

            try:
                lang, topic = name.split('_')
            except ValueError:
                self.notify.error('Failed to load localizer csv. %s has broken formatting. (expected <lang_topic.csv)' % name)

            self.__add_topic(id, topic)

            fh = codecs.open(csv_file, 'r', encoding=self.__encoding)
            reader = unicode_csv_reader(fh, delimiter=self.__delimiter, quotechar='"', skipinitialspace=True)
            by_id = {}
            by_name = {}
            last_succesful = ['', '']

            try: 
                for line_nr, line in enumerate(reader):
                    if len(line) == 3:
                        if line[0].isdigit():
                            by_id[int(line[0])] = line[2]
                        by_name[line[1]] = line[2]
                        last_succesful = [line[0], line[1]]
                    else:
                        self.notify.info('Last succesful read: %s %s.' % (last_succesful[0], last_succesful[1]))
                        self.notify.error('Failed to read file "%s.csv" on line #%s' % (name, line_nr + 1))
            except Exception as e:
                self.notify.error('Failed to read file "%s.csv. Reason: %s' % (name, e))

            fh.close()
            if lang not in self.__resources:
                self.__resources[lang] = {}
            self.__resources[lang][topic] = (by_id, by_name)
            
            if not self.__active_language:
                self.__active_language = lang

    def __add_topic(self, id: object, topic: object) -> None:
        """
        """

        setattr(self, self.__build_get_name(topic), lambda id, topic = topic, **kw: self.__get(topic=topic, id=id, **kw))
        setattr(ApplicationLocalizer, self.__build_get_name(topic), staticmethod(lambda id, topic = topic, **kw: ApplicationLocalizer.__get(ApplicationLocalizer.get_singleton(), topic=topic, id=id, **kw)))
        setattr(self, self.__build_has_name(topic), lambda id, topic = topic: self.__has(topic=topic, id=id))
        setattr(ApplicationLocalizer, self.__build_has_name(topic), staticmethod(lambda id, topic = topic: ApplicationLocalizer.__has(ApplicationLocalizer.get_singleton(), topic=topic, id=id)))

    def destroy(self) -> None:
        """
        Called on localizer destruction
        """

    def __build_method_name(self, action: str, topic: str) -> str:
        """
        """

        return '%s_%s' % (action, get_snake_case(topic))

    def __build_get_name(self, topic: str) -> str:
        """
        """

        return self.__build_method_name('get', topic)

    def __build_has_name(self, topic: str) -> str:
        """
        """

        return self.__build_method_name('has', topic)

    def __attempt_delete_attr(self, space: object, attr: str) -> None:
        """
        """

        try:
            delattr(space, attr)
        except AttributeError:
            pass

    def __del_attr(self, attr: str) -> None:
        """
        """

        self.__attempt_delete_attr(self, attr)
        self.__attempt_delete_attr(self.__class__, attr)
        
    def set_encoding(self, encoding: str) -> None:
        """
        """

        self.__encoding = encoding

    def get_encoding(self) -> str:
        """
        """

        return self.__encoding

    def set_active_language(self, lang: str) -> None:
        """
        """

        if lang in self.__resources:
            self.notify.info('Setting active language: %s' % lang)
            self.__active_language = lang
        else:
            self.notify.warning('Failed to set active language. Unknown language: %s' % (lang))

    def get_active_language(self) -> str:
        """
        """

        return self.__active_language
    
    def get_all_languages(self) -> list:
        """
        """

        return list(self.__resources.keys())

    def __get_keys(self, lang: str, topic: str) -> tuple:
        """
        """

        if not len(self.__resources):
            self.notify.warning('Failed to retrieve keys. No language data loaded')
            return ([], [])

        if lang in self.__resources:
            language_set = self.__resources[lang]
            if topic in language_set:
                topic_set = language_set[topic]
                return (topic_set[0], topic_set[1])
            else:
                self.notify.warning('Failed to retrieve keys. Unknown topic "%s"' % topic)
        elif self.__warnings:
            self.notify.warning('Failed to retrieve keys. Unknown language "%s"' % lang) 

        return ([], [])

    def get_id_keys(self, lang: str, topic: str) -> list:
        """
        """

        by_id, by_name = self.__get_keys(lang, topic)
        return list(by_id.keys())

    def get_name_keys(self, lang: str, topic: str) -> list:
        """
        """

        by_id, by_name = self.__get_keys(lang, topic)
        return list(by_name.keys())

    def get_keys(self, lang: str, topic: str) -> list:
        """
        """

        by_id, by_name = self.__get_keys(lang, topic)
        return list(by_id.keys()) + list(by_name.keys())

    def __get_template(self, topic: str, id: object) -> object:
        """
        """

        return self.__get_language_template(topic, id, self.__active_language)

    def __get_language_template(self, topic: str, id: object, lang: str) -> object:
        """
        """

        if lang is not None:
            lang = self.__active_language

        result = None
        by_id, by_name = self.__get_keys(lang, topic)

        if id in by_id:
            result = by_id[id]
        
        if id in by_name:
            result = by_name[id]

        return result

    def __decode_special(self, m: object) -> object:
        """
        """

        x = m.group(0)[1:]
        return chr(int(x))

    def __get(self, topic: object, id: object, **kw) -> None:
        """
        """

        result = ApplicationLocalizer.get_backup_text()
        template = self.__get_language_template(topic, id, kw.get('client_language', self.__active_language))
        if template is not None:
            if self.__encoding is None:
                result = template
            else:
                result = template.encode(self.__encoding)

            if kw:
                try:
                    result = string.Template(result).safe_substitute(kw)
                except Exception as e:
                    self.notify.error('Encoding failed: %s (id: %s, kw: %s)' % (id, repr(kw)))

        if not isinstance(result, str):
            result = result.decode(self.__encoding)

        result = result.replace('\\n', '\n')
        return result

    def __has(self, topic: object, id: object) -> object:
        """
        Returns true if the requested topic exists
        """

        return self.__get_template(topic, id) is not None

    def __getattr__(self, key) -> None:
        """
        Custom attribute handler for warning of unknown localizations
        """

        action = key[:3]
        topic = key[4:].lower()

        if action == 'get':
            self.notify.warning('Unknown localization topic: "%s"' % topic)
            return lambda *args, **kw: str('Localization Error')
        elif action == 'has':
            self.notify.warning('Unknown localization topic: "%s"' % topic)
            return lambda *args, **kw: False

        raise AttributeError('%s has no attribute "%s"' % (
            self.__class__.__name__, key))