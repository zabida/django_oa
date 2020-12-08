def query_trade_good_old(request):
    user_info = request.session[my_enums.LOGIN_USER_CACHE_KEY]
    import json
    print(json.dumps(user_info))
    centerId = user_info["centerId"]
    memId = user_info["memId"]
    cursor = connection.cursor()
    tagType = request.REQUEST.get("type")
    pcode = request.REQUEST.get("pcode")
    name = request.REQUEST.get("name")

    commonTag = Tag.objects.filter(status=my_enums.TAG_STATUS_ACTIVE, tagType=tagType)

    prdt_list_em = Tag.objects.none()
    # 通过关键词or name 筛选
    if name:
        text_list = name.split(" ")
        for text_excerpt in text_list:
            prdt_list_em |= commonTag.filter(name__contains=text_excerpt)

        commonTag = prdt_list_em

    if pcode:
        cat_code_list = Catgory.objects.get(code=pcode).allChildrenCode()
        commonTag = commonTag.filter(parent_code__in=cat_code_list)
    # 供方数过滤
    tagList = []
    tagSupCount = {}
    tagObjectId = {}
    center_mem_id = eval(get_config_value("common", "center_mem_id"))  # 中心帐号列表
    prdt_show_mem_id_dict = eval(get_config_value("common", "prdt_show_mem_id"))  # 互联对象显示白名单字典
    for tag in commonTag:

        if (tag.type == my_enums.TAG_TYPE_NORMAL) or (memId in center_mem_id):  # 差价模式下的 01其它类别或会员为中心
            if centerId != 1:
                a = "SELECT DISTINCT spbi.connObjId FROM sup_prdt_base_info spbi, access_member_base_info mem" \
                    " WHERE spbi.supMemId=mem.memId AND spbi.status=%s AND spbi.prdtIdCd=%s " \
                    "AND mem.centerId=%s;" % (my_enums.PRDT_STATUS_ACTIVE, tag.code, centerId)
                print(111, a)
                cursor.execute(
                    "SELECT DISTINCT spbi.connObjId FROM sup_prdt_base_info spbi, access_member_base_info mem WHERE spbi.supMemId=mem.memId AND spbi.status=%s AND spbi.prdtIdCd=%s AND mem.centerId=%s;",
                    [my_enums.PRDT_STATUS_ACTIVE, tag.code, centerId])
            else:
                cursor.execute(
                    "SELECT DISTINCT spbi.connObjId FROM sup_prdt_base_info spbi, access_member_base_info mem WHERE spbi.supMemId=mem.memId AND spbi.status=%s AND spbi.prdtIdCd=%s;",
                    [my_enums.PRDT_STATUS_ACTIVE, tag.code])

        else:  # 差价模式下的服务类,且会员不是中心
            prdtList = PrdtBaseInfo.objects.filter(prdtIdCd=tag.code, status=my_enums.PRDT_STATUS_ACTIVE)
            prdtCodeList = []
            for prdt in prdtList:
                if (memId in prdt_show_mem_id_dict.get(prdt.connObjId, [])) or (prdt.supMemId == memId):
                    prdtCodeList.append(prdt.connObjId.encode("utf8"))
            if prdtCodeList:
                listStr = '"' + '","'.join(prdtCodeList) + '"'
                if centerId != 1:
                    sql_str = 'SELECT DISTINCT spbi.connObjId FROM sup_prdt_base_info spbi, access_member_base_info mem WHERE spbi.supMemId=mem.memId and spbi.connObjId in (%s)' % (
                        listStr)
                    cursor.execute(
                        sql_str + ' AND mem.centerId=%s;', [centerId])
                else:
                    cursor.execute(
                        "SELECT DISTINCT spbi.connObjId FROM sup_prdt_base_info WHERE connObjId in (%s) ", [listStr])
            else:
                continue
        connObjIdTuple = cursor.fetchall()
        connObjIdTupleLen = len(connObjIdTuple)
        if connObjIdTupleLen > 0:
            code = tag.code
            tagList.append(code)
            tagSupCount[code] = connObjIdTupleLen
            connObjIdList = []
            for idTuple in connObjIdTuple:
                connObjIdList.append(idTuple[0].encode('utf8'))
            tagObjectId[code] = '"' + '","'.join(connObjIdList) + '"'
    print(112, tagList)
    commonTag = commonTag.filter(code__in=tagList)
    commonTag = common_list(request, commonTag)
    list = []
    for tagItem in commonTag["list"]:
        item = {}
        item["name"] = tagItem.name
        item["valueDesc"] = tagItem.value_ex
        item["prdtIdCd"] = tagItem.code
        item["apiFile"] = str(tagItem.apiFile)
        if tagType == my_enums.PRDT_SCEN_CREDIT:
            typeList = []
            crpTag = CrpTag.objects.filter(code=tagItem.code)
            if len(crpTag) > 0:
                item["prdtDesc"] = crpTag[0].description

            crpIdList = CrpID.objects.filter(tagCode=tagItem.code)
            for crpId in crpIdList:
                idObjList = IDObj.objects.filter(code=crpId.idCode)
                for idObj in idObjList:
                    typeList.append(idObj.name)

            item["idType"] = ','.join(typeList)

        try:
            # cursor.execute(
            #     "SELECT COUNT(DISTINCT spbi.supMemId) FROM sup_prdt_base_info spbi WHERE spbi.status=%s AND spbi.prdtIdCd=%s;", [my_enums.PRDT_STATUS_ACTIVE, tagItem.code])
            # count = cursor.fetchone()
            item["supMemCount"] = tagSupCount[tagItem.code]

            # 2018-10-18 运营优化
            param = []
            param.append(tagItem.code)
            param.append(my_enums.PRDT_STATUS_ACTIVE)
            strSql = "select valuationModeCd,valuationPrice,valuationCountCd from sup_prdt_val_mode spvm left join sup_prdt_base_info spbi on spbi.connObjNo= spvm.connObjNo left join access_member_base_info mem on spbi.supMemId = mem.memId where spbi.connObjId in (%s)" % (
                tagObjectId.get(tagItem.code))
            print(211, centerId, strSql)
            if centerId != 1:
                param.append(centerId)
                # b = strSql + " and spbi.prdtIdCd=%s and spbi.status=%s and mem.centerId=%s;" % (param[0], param[1], param[2])
                # print(122, b)
                cursor.execute(
                    strSql + " and spbi.prdtIdCd=%s and spbi.status=%s and mem.centerId=%s;", param)
            else:
                cursor.execute(
                    strSql + " and spbi.prdtIdCd=%s and spbi.status=%s;", param)
            results = cursor.fetchall()
            max = Decimal(0.000)
            min = Decimal(0.000)
            sum = Decimal(0.000)
            count = 0
            for row in results:
                count = count + 1
                modeCd = row[0]
                price = row[1]
                if count == 1:
                    min = price
                if modeCd in (u"02", u"05"):
                    price = row[1] / 1000
                if price > max:
                    max = price
                if price < min:
                    min = price
                sum = sum + price
            avg = sum / count
            item["maxPrice"] = str(max.quantize(Decimal('0.000')))
            item["minPrice"] = str(min.quantize(Decimal('0.000')))
            item["avgPrice"] = str(avg.quantize(Decimal('0.000')))
        except Exception:
            item["supMemCount"] = 0

        list.append(item)

    commonTag["list"] = list
    commonTag.pop("request")

    return commonTag


def query_trade_good_with_detail(request):
    """供方编号查询交易物品"""
    user_info = request.session[my_enums.LOGIN_USER_CACHE_KEY]
    centerId = user_info["centerId"]
    memId = user_info["memId"]
    tagType = request.REQUEST.get("type")
    pcode = request.REQUEST.get("pcode")
    name = request.REQUEST.get("name")
    sup_mem_id = request.REQUEST.get('supMemId')
    cursor = connection.cursor()
    common_tag = Tag.objects.filter(status=my_enums.TAG_STATUS_ACTIVE, tagType=tagType)

    prdt_list_em = Tag.objects.none()
    # 通过关键词or name 筛选
    if name:
        text_list = name.split(" ")
        for text_excerpt in text_list:
            prdt_list_em |= common_tag.filter(name__contains=text_excerpt)

        common_tag = prdt_list_em

    if pcode:
        cat_code_list = Catgory.objects.get(code=pcode).allChildrenCode()
        common_tag = common_tag.filter(parent_code__in=cat_code_list)
    # 供方数过滤
    tag_list = []
    tag_sup_count = dict()
    tag_object_id = dict()
    center_mem_id = eval(get_config_value("common", "center_mem_id"))  # 中心帐号列表
    prdt_show_mem_id_dict = eval(get_config_value("common", "prdt_show_mem_id"))  # 互联对象显示白名单字典
    for tag in common_tag:

        if (tag.type == my_enums.TAG_TYPE_NORMAL) or (memId in center_mem_id):  # 差价模式下的 01其它类别或会员为中心
            if centerId != 1:
                sql_ = "SELECT DISTINCT spbi.connObjId FROM sup_prdt_base_info spbi, access_member_base_info mem" \
                       " WHERE spbi.supMemId=mem.memId AND spbi.status=%s AND spbi.prdtIdCd=%s " \
                       "AND mem.centerId=%s AND spbi.supMemId=%s;" % \
                       (my_enums.PRDT_STATUS_ACTIVE, tag.code, centerId, sup_mem_id)
                print(111, sql_)
                cursor.execute(sql_)
            else:
                sql_ = "SELECT DISTINCT spbi.connObjId FROM sup_prdt_base_info spbi, access_member_base_info mem " \
                       "WHERE spbi.supMemId=mem.memId AND spbi.status=%s AND spbi.prdtIdCd=%s " \
                       "AND spbi.supMemId=%s" % (my_enums.PRDT_STATUS_ACTIVE, tag.code, sup_mem_id)
                print(112, sql_)
                cursor.execute(sql_)
        else:  # 差价模式下的服务类,且会员不是中心
            prdt_list = PrdtBaseInfo.objects.filter(prdtIdCd=tag.code, status=my_enums.PRDT_STATUS_ACTIVE)
            prdt_code_list = []
            for prdt in prdt_list:
                if (memId in prdt_show_mem_id_dict.get(prdt.connObjId, [])) or (prdt.supMemId == memId):
                    prdt_code_list.append(prdt.connObjId.encode("utf8"))
            if prdt_code_list:
                list_str = '"{}"'.format('","'.join(prdt_code_list))
                print(113, list_str)
                if centerId != 1:
                    sql_ = 'SELECT DISTINCT spbi.connObjId FROM sup_prdt_base_info spbi, ' \
                           'access_member_base_info mem WHERE spbi.supMemId=mem.memId ' \
                           'and spbi.connObjId in (%s) AND mem.centerId=%s AND spbi.supMemId=%s;' % \
                           (list_str, centerId, sup_mem_id)
                    cursor.execute(sql_)
                else:
                    sql_ = "SELECT DISTINCT spbi.connObjId FROM sup_prdt_base_info " \
                           "WHERE connObjId in (%s) AND spbi.supMemId=%s;" % (list_str, sup_mem_id)
                    cursor.execute(sql_)
            else:
                print(114)
                continue
        conn_obj_id_tuple = cursor.fetchall()
        conn_obj_id_tuple_len = len(conn_obj_id_tuple)
        if conn_obj_id_tuple_len > 0:
            code = tag.code
            tag_list.append(code)
            tag_sup_count[code] = conn_obj_id_tuple_len
            conn_obj_id_list = [id_tuple[0].encode('utf8') for id_tuple in conn_obj_id_tuple]
            tag_object_id[code] = '"' + '","'.join(conn_obj_id_list) + '"'

    # 按供方编号搜索，查prdt_base_info表，根据编号查
    print(210, tag_list)
    common_tag = common_tag.filter(code__in=tag_list)
    common_tag = common_list(request, common_tag)
    list = []
    for tag_item in common_tag["list"]:
        item = {}
        item["name"] = tag_item.name
        item["valueDesc"] = tag_item.value_ex
        item["prdtIdCd"] = tag_item.code
        item["apiFile"] = str(tag_item.apiFile)
        if tagType == my_enums.PRDT_SCEN_CREDIT:
            type_list = []
            crp_tag = CrpTag.objects.filter(code=tag_item.code)
            if len(crp_tag) > 0:
                item["prdtDesc"] = crp_tag[0].description

            crp_id_list = CrpID.objects.filter(tagCode=tag_item.code)
            for crp_id in crp_id_list:
                id_obj_list = IDObj.objects.filter(code=crp_id.idCode)
                for id_obj in id_obj_list:
                    type_list.append(id_obj.name)

            item["idType"] = ','.join(type_list)

        try:
            item["supMemCount"] = tag_sup_count[tag_item.code]

            # 2018-10-18 运营优化
            param = []
            param.append(tag_item.code)
            param.append(my_enums.PRDT_STATUS_ACTIVE)
            str_sql = "select valuationModeCd,valuationPrice,valuationCountCd from sup_prdt_val_mode spvm " \
                      "left join sup_prdt_base_info spbi on spbi.connObjNo= spvm.connObjNo " \
                      "left join access_member_base_info mem on spbi.supMemId = mem.memId " \
                      "where spbi.connObjId in (%s)" % tag_object_id.get(tag_item.code)
            if centerId != 1:
                param.append(centerId)
                sql_ = str_sql + " and spbi.prdtIdCd=%s and spbi.status=%s and mem.centerId=%s;" % (
                param[0], param[1], param[2])
                cursor.execute(sql_)
            else:
                sql_ = str_sql + " and spbi.prdtIdCd=%s and spbi.status=%s;" % (param[0], param[1])
                cursor.execute(sql_)
            results = cursor.fetchall()
            max = Decimal(0.000)
            min = Decimal(0.000)
            sum = Decimal(0.000)
            count = 0
            for row in results:
                count = count + 1
                modeCd = row[0]
                price = row[1]
                if count == 1:
                    min = price
                if modeCd in (u"02", u"05"):
                    price = row[1] / 1000
                if price > max:
                    max = price
                if price < min:
                    min = price
                sum = sum + price
            avg = sum / count
            item["maxPrice"] = str(max.quantize(Decimal('0.000')))
            item["minPrice"] = str(min.quantize(Decimal('0.000')))
            item["avgPrice"] = str(avg.quantize(Decimal('0.000')))
        except Exception:
            item["supMemCount"] = 0

        list.append(item)

    common_tag["list"] = list
    common_tag.pop("request")

    return common_tag


@user_login_required
@has_Permission_User([u"交易大厅查询"])
@render_to_json
def query_trade_goods(request):
    """交易品列表查询"""
    sup_mem_id = request.REQUEST.get('supMemId')
    if sup_mem_id:
        common_tag = query_trade_good_with_detail(request)
    else:
        common_tag = query_trade_good_old(request)
    return getResultCode(common_tag)