import logging
import random

from ...engines_interact.abstract.dbhelper import DBHelper
from ....settings import parameters
from .mysql import MySqlClient

logger = logging.getLogger(__name__)
Types = parameters.Types


class DBHelperMySQL(DBHelper):
    """
    This class inherits from DBHelper and make an interaction with mysql database server.
    """

    def __init__(self):
        super().__init__()
        self._dbclient = MySqlClient()

    # working
    def get_category_id_by_cat_name(self, cat_name):
        """Get category's id by category's name.

        :param cat_name: [string]: The category's name.

        :return: id: [int]. The id of the category.
        :rtype int
        """
        table = 'category'
        query = 'SELECT id FROM ' + table + " WHERE name=N'" + cat_name + "'"
        datatable = self._dbclient.select(query=query)
        if datatable != None and len(datatable) > 0:
            row = datatable[0]  # get the first row
            return row[0]  # get the id from the row
        else:
            return -1

    def get_sub_categories_and_ids(self, parent_id):
        """Get all sub-categories of one category if parent-id is known.

        :param parent_id: [int]. The parent-id.

        :return: The ids and names of all sub-categories.
        """
        table = 'category'
        query = "SELECT id, name FROM " + table + " WHERE parent_id='" + str(parent_id) + "'"
        datatable = self._dbclient.select(query=query)
        if datatable != None and len(datatable) > 0:
            id_cat = dict()
            # ids = list()
            # categories = list()
            for i in range(len(datatable)):
                row = datatable[i]
                id_value = row[0]
                category = row[1]
                id_cat[id_value] = category
                # ids.append(id_value)
                # categories.append(category)
            return id_cat  # ids, categories
        else:
            return None  # , None

    def __get_json_from_support_row(self, row, type):
        result = dict()
        if str(type).__eq__(Types.type_acknowledgment):
            result['title'] = row[0]
            result['content'] = row[1]
        elif str(type).__eq__(Types.type_mobile):
            result['title'] = row[0]
            result['content'] = row[1]
            result['example'] = row[2]
            result['note'] = row[3]
            result['prevention'] = row[4]
        elif str(type).__eq__(Types.type_threat):
            result['title'] = row[0]
            result['content'] = row[1]
            result['example'] = row[2]
            result['note'] = row[3]
            result['prevention'] = row[4]
        else:
            pass
        return result

    def __get_json_type_from_support_row(self, row):
        if row is None:
            return
        result = dict()
        res_type = None
        try:
            title = row[0]
            content = row[1]
            example = row[2]
            note = row[3]
            prevention = row[4]
            url = row[5]
            type = row[6]
            if type == 'text':
                result['title'] = title
                result['content'] = content
                res_type = Types.type_text
            elif type == 'image':
                result['title'] = title
                result['url'] = url
                res_type = Types.type_image
            elif type == 'video':
                result['title'] = title
                result['url'] = url
                res_type = Types.type_video
            elif type == 'audio':
                result['title'] = title
                result['url'] = url
                res_type = Types.type_audio
        except:
            result = None
            res_type = Types.type_text
        return result, res_type

    def get_acknowledgment_device(self, device_name):
        """
        Get settings device acknowledgment

        :param device_name: The device name

        :return: The json-type of device information
        """
        table = 'support'
        query = 'SELECT title, content, example, note, prevention, url, type FROM ' + table + ' WHERE title=N\'' + device_name + '\''
        datatable = self._dbclient.select(query=query)
        if datatable != None:
            if len(datatable) > 1:
                i = random.randint(0, len(datatable))
                row = datatable[i]
            else:
                row = datatable[0]
            # result = self.__get_json_from_support_row(row=row, type=parameters.type_acknowledgment)
            result, type = self.__get_json_type_from_support_row(row=row)
            return result, type  # json.dumps(result)
        else:
            return None, None

    def get_acknowledgment_os(self, os_name):
        """
        Get settings operating system acknowledgment.

        :param os_name: The name of operating system.

        :return: The json-type of operating system information.
        """
        table = 'support'
        query = 'SELECT title, content, example, note, prevention, url, type FROM ' + table + ' WHERE title=N\'' + os_name + '\''
        datatable = self._dbclient.select(query=query)
        if datatable != None:
            if len(datatable) > 1:
                i = random.randint(0, len(datatable))
                row = datatable[i]
            else:
                row = datatable[0]
            # result = self.__get_json_from_support_row(row=row, type=parameters.type_acknowledgment)
            result, type = self.__get_json_type_from_support_row(row=row)
            return result, type  # json.dumps(result)
        else:
            return None, None

    def get_acknowledgment_software(self, software_name):
        """
        Get settings operating system acknowledgment.

        :param software_name: The name of operating system.

        :return: The json-type of operating system information.
        """
        table = 'support'
        query = 'SELECT title, content, example, note, prevention, url, type FROM ' + table + ' WHERE title=N\'' + software_name + '\''
        datatable = self._dbclient.select(query=query)
        if datatable != None:
            if len(datatable) > 1:
                i = random.randint(0, len(datatable))
                row = datatable[i]
            else:
                row = datatable[0]
            # result = self.__get_json_from_support_row(row=row, type=parameters.type_acknowledgment)
            result, type = self.__get_json_type_from_support_row(row=row)
            return result, type  # json.dumps(result)
        else:
            return None, None

    def get_mobile_info(self, os_name):
        """Get mobile information by os name.

        :param os_name: The name of operating system.

        :return: The json-format result.
        """
        # result = dict()
        # result['title'] = 'threat'
        # result['url'] = 'https://traffic.libsyn.com/securitypodcast/5777.mp3'
        # res_type = parameters.type_audio
        # return result, res_type
        table = 'support'
        query = 'SELECT title, content, example, note, prevention, url, type FROM ' + table + ' WHERE title=N\'' + os_name + '\''
        datatable = self._dbclient.select(query=query)
        if datatable != None:
            # return json.dumps(datatable)
            if len(datatable) > 1:
                i = random.randint(0, len(datatable))
                row = datatable[i]
            else:
                row = datatable[0]
            # result = self.__get_json_from_support_row(row=row, type=parameters.type_mobile)
            result, type = self.__get_json_type_from_support_row(row=row)
            return result, type  # json.dumps(result)
        else:
            return None, None

    def get_mobile_threat(self, os_name):
        """Get mobile threats by os name.

        :param os_name: The name of operating system.

        :return: The json-format result.
        """
        # result = dict()
        # result['title'] = 'threat'
        # result['url'] = 'https://www.youtube.com/watch?v=ouGLJSDGQsk'
        # res_type = parameters.type_video
        # return result, res_type

        keyword = 'threat'
        cat_id = self.get_category_id_by_cat_name(cat_name=keyword)
        id_cats = self.get_sub_categories_and_ids(parent_id=cat_id)
        found_cat_id = None
        for key in id_cats.keys():
            value = id_cats[key]
            if str(value).lower() == str(os_name).lower():
                found_cat_id = key
                break
        if found_cat_id:
            table = 'support'
            query = 'SELECT title, content, example, note, prevention, url, type FROM ' + table + ' WHERE category_id=\'' + str(
                found_cat_id) + '\''
            datatable = self._dbclient.select(query=query)
            if datatable != None:
                # return only one of records in database
                if len(datatable) > 1:
                    i = random.randint(0, len(datatable))
                    row = datatable[i]
                    # return json.dumps(row)
                else:
                    row = datatable[0]
                    # return json.dumps(datatable[0])
                # result = self.__get_json_from_support_row(row=row, type=parameters.type_mobile)
                result, type = self.__get_json_type_from_support_row(row=row)
                return result, type  # json.dumps(result)
            else:
                return None, None
        else:
            return None, None

    def get_mobile_tips(self, os_name):
        """Get tips for mobile device by os name.

        :param os_name: The os name

        :return: The json-format of result.
        """
        # result = dict()
        # result['title'] = 'tips'
        # result['url'] = 'https://www.it-market.com/media/images/org/c_ASR1001X_10G_K9_640_x_480_1.jpg'
        # res_type = parameters.type_image
        # return result, res_type
        keyword = 'tips'
        cat_id = self.get_category_id_by_cat_name(cat_name=keyword)
        id_cats = self.get_sub_categories_and_ids(parent_id=cat_id)
        found_cat_id = None
        for key in id_cats.keys():
            value = id_cats[key]
            if str(value).lower() == str(os_name).lower():
                found_cat_id = key
                break
        if found_cat_id:
            table = 'support'
            query = 'SELECT title, content, example, note, prevention, url, type FROM ' + table + ' WHERE category_id=\'' + str(
                found_cat_id) + '\''
            datatable = self._dbclient.select(query=query)
            if datatable != None:
                # return only one of records in database
                if len(datatable) > 1:
                    i = random.randint(0, len(datatable))
                    row = datatable[i]
                    # return json.dumps(row)
                else:
                    row = datatable[0]
                    # return json.dumps(datatable[0])
                # result = self.__get_json_from_support_row(row=row, type=parameters.type_mobile)
                result, type = self.__get_json_type_from_support_row(row=row)
                return result, type  # json.dumps(result)
            else:
                return None, None
        else:
            return None, None

            # table = 'threat'
            # query = 'SELECT * FROM ' + table + ' WHERE device_name=\'' + os_name+'\''
            # datatable = self._dbclient.select(query=query)
            # if datatable != None:
            #     return json.dumps(datatable)
            # else:
            #     return None

    def get_tips(self, tip_name):
        pass
