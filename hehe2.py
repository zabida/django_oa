@user_login_required
@has_Permission_User([u"交易大厅查询"])
@render_to_json
def query_trade_goods(request):
    """交易品列表查询"""
    user_info = request.session[my_enums.LOGIN_USER_CACHE_KEY]
    centerId = user_info["centerId"]
    memId = user_info["memId"]
    cursor = connection.cursor()
    tagType = request.REQUEST.get("type")
    pcode = request.REQUEST.get("pcode")
    name = request.REQUEST.get("name")
    supMemId = request.REQUEST.get('supMemId')
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

        if (tag.type == my_enums.TAG_TYPE_NORMAL) or (memId in center_mem_id):  # 差价模式下的其它类别或会员为中心
            sql_ = "SELECT DISTINCT spbi.connObjId FROM sup_prdt_base_info spbi, access_member_base_info mem " \
                   "WHERE spbi.supMemId=mem.memId AND spbi.status=%s AND spbi.prdtIdCd=%s " \
                   % (my_enums.PRDT_STATUS_ACTIVE, tag.code)
            if centerId != 1:
                sql_ = sql_ + " AND mem.centerId=%s" % centerId
                if supMemId:
                    sql_ = sql_ + " AND spbi.supMemId=%s" % supMemId
                cursor.execute(sql_)
            else:
                if supMemId:
                    sql_ = sql_ + " AND spbi.supMemId=%s" % supMemId
                cursor.execute(sql_)

        else:  # 差价模式下的服务类 ,且会员不是中心
            prdtList = PrdtBaseInfo.objects.filter(prdtIdCd=tag.code, status=my_enums.PRDT_STATUS_ACTIVE)
            ConnObjIdList = []
            for prdt in prdtList:
                if (memId in prdt_show_mem_id_dict.get(prdt.connObjId, [])) or (prdt.supMemId == memId):
                    ConnObjIdList.append(prdt.connObjId.encode("utf8"))
            if ConnObjIdList:
                conn_obj_ids_str = '"{}"'.format('","'.join(ConnObjIdList))
                if centerId != 1:
                    sql_ = 'SELECT DISTINCT spbi.connObjId FROM sup_prdt_base_info spbi, access_member_base_info mem ' \
                           ' WHERE spbi.supMemId=mem.memId AND spbi.connObjId in (%s) AND mem.centerId=%s ' \
                           % (conn_obj_ids_str, centerId)
                    if supMemId:
                        sql_ = sql_ + " AND spbi.supMemId=%s" % supMemId
                    cursor.execute(sql_)
                else:
                    sql_ = "SELECT DISTINCT spbi.connObjId FROM sup_prdt_base_info sbpi" \
                           " WHERE connObjId in (%s) " % conn_obj_ids_str
                    if supMemId:
                        sql_ = sql_ + " AND spbi.supMemId=%s" % supMemId
                    cursor.execute(sql_)
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
            tagObjectId[code] = '"{}"'.format('","'.join(connObjIdList))

    commonTag = commonTag.filter(code__in=tagList)
    commonTag = common_list(request, commonTag)
    list_ = []
    for tagItem in commonTag["list"]:
        item = dict()
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
            #     "SELECT COUNT(DISTINCT spbi.supMemId) FROM sup_prdt_base_info spbi
            #     WHERE spbi.status=%s AND spbi.prdtIdCd=%s;", [my_enums.PRDT_STATUS_ACTIVE, tagItem.code])
            # count = cursor.fetchone()
            item["supMemCount"] = tagSupCount[tagItem.code]

            # 2018-10-18 运营优化
            sql_ = "select valuationModeCd,valuationPrice,valuationCountCd from sup_prdt_val_mode spvm " \
                   "left join sup_prdt_base_info spbi on spbi.connObjNo= spvm.connObjNo " \
                   "left join access_member_base_info mem on spbi.supMemId = mem.memId " \
                   "where spbi.connObjId in (%s)" % tagObjectId.get(tagItem.code)
            if centerId != 1:
                sql_ = sql_ + " and spbi.prdtIdCd=%s and spbi.status=%s and mem.centerId=%s;" % \
                       tagItem.code, my_enums.PRDT_STATUS_ACTIVE, centerId
                cursor.execute(sql_)
            else:
                sql_ = sql_ + " and spbi.prdtIdCd=%s and spbi.status=%s;" % tagItem.code, my_enums.PRDT_STATUS_ACTIVE
                cursor.execute(sql_)

            results = cursor.fetchall()
            max_ = Decimal(0.000)
            min_ = Decimal(0.000)
            sum_ = Decimal(0.000)
            count_ = 0
            for row in results:
                count_ += 1
                modeCd = row[0]
                price = row[1]
                if count_ == 1:
                    min_ = price
                if modeCd in (u"02", u"05"):
                    price = row[1] / 1000
                if price > max_:
                    max_ = price
                if price < min_:
                    min_ = price
                sum_ = sum_ + price
            avg_ = sum_ / count_
            item["maxPrice"] = str(max_.quantize(Decimal('0.000')))
            item["minPrice"] = str(min_.quantize(Decimal('0.000')))
            item["avgPrice"] = str(avg_.quantize(Decimal('0.000')))
        except Exception:
            item["supMemCount"] = 0

        list_.append(item)

    commonTag["list"] = list_
    commonTag.pop("request")
    return getResultCode(commonTag)