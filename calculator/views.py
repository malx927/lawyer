import datetime
import decimal

from django.forms import formset_factory
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from calculator.constants import HOUSEHOLD_TYPE, DUTY_TYPE, DISABILITY_TYPE
from calculator.forms import DisabilityForm, CalculatorUserForm, SupportedFormSet, RelationFormSet
from calculator.models import AreaCode, Industry, ResIncomeExpend
from lawyer import settings


NUTRITION_WAGE = 50
MAX_YEARS = 80
MAX_PAY_YEARS = 20


class CalculatorView(View):
    """计算首页"""
    def get(self, request, *args, **kwargs):

        return render(request, template_name="calculator/index.html")


class TrafficCalcView(View):
    """交通计算"""

    def get(self, request, *args, **kwargs):
        house_type = dict(HOUSEHOLD_TYPE)
        duty_type = dict(DUTY_TYPE)
        province_list = AreaCode.objects.extra(where=['length(code)=2'])
        city_list = AreaCode.objects.extra(where=['length(code)=4'])
        industries = Industry.objects.all()
        return render(request, template_name="calculator/traffic.html", context=locals())

    def post(self, request, *args, **kwargs):
        age = request.POST.get("age", None)  # 年龄
        dead = request.POST.get("dead", None)  # 是否死亡
        funeral_expense = request.POST.get("funeral_expense", None)  # 丧葬费
        house_type = request.POST.get("house_type", None)  # 户口属性
        province = request.POST.get("province", None)  # 住所地省
        city = request.POST.get("city", None)  # 所在市
        court_province = request.POST.get("court_province", None)  # 受案法院所在地省
        court_city = request.POST.get("court_city", None)  # 所在市
        # city_house = request.POST.get("city_house", None)  # 同一事故中是否有城镇户口
        # one_years = request.POST.get("one_years", None)  # 是否在城镇居住一年以上
        # stable_income = request.POST.get("stable_income", None)  # 一年以上稳定工资收入证明
        exec_house = request.POST.get("exec_house", None)  # 执行标准
        fix_income = request.POST.get("fix_income", None)  # 是否有固定收入
        fix_income_money = request.POST.get("fix_income_money", None)  # 日收入金额
        prove_income = request.POST.get("prove_income", None)  # 举证三年收入的平均日收入
        industry = request.POST.get("industry", None)  # 从事的行业
        industry_wage = request.POST.get("industry_wage", None)  # 行业收入
        spirit_fee = request.POST.get("spirit_fee", None)  # 精神抚慰金
        other_fee = request.POST.get("other_fee", None)  # 其他费用

        car_type = request.POST.get("car_type", None)  # 对方车辆类型
        insure = request.POST.get("insure", None)  # 对方是否有保险
        asset_lost = request.POST.get("asset_lost", None)  # 财产损失
        duty_confirm = request.POST.get("duty_confirm", None)  # 责任认定

        calculator = {
            "age": age,
            "dead": dead,
            "funeral_expense": funeral_expense,
            "house_type": house_type,
            "province": province,
            "city": city,
            "court_province": court_province,
            "court_city": court_city,
            # "city_house": city_house,
            # "one_years": one_years,
            # "stable_income": stable_income,
            "exec_house": exec_house,
            "fix_income": fix_income,
            "fix_income_money": fix_income_money,
            "prove_income": prove_income,
            "industry": industry,
            "industry_wage": industry_wage,
            "spirit_fee": spirit_fee,
            "other_fee": other_fee,
        }
        request.session[settings.CALCULATOR_SESSION_KEY] = calculator
        return redirect(reverse("calculator:hospital-index"))


class HospitalCalcView(View):
    """住院信息计算"""
    def get(self, request, *args, **kwargs):
        return render(request, template_name="calculator/hospital.html", )

    def post(self, request, *args, **kwargs):
        enter_time = request.POST.get("enter_time", None)  # 入院日期
        leave_time = request.POST.get("leave_time", None)  # 出院日期
        hospital_day = request.POST.get("hospital_day", None)  # 住院天数
        hospital_costs = request.POST.get("hospital_costs", None)  # 医药费、治疗费
        rest_day = request.POST.get("rest_day", None)  # 医嘱中需要休养天数
        nutrition = request.POST.get("nutrition", None)  # 医嘱中是否需加强营养
        device_cost = request.POST.get("device_cost", None)  # 辅助器具的金额
        device_period = request.POST.get("device_period", None)  # 辅助器具更换期
        car_fee = request.POST.get("car_fee", None)  # 交通费
        hotel_fee = request.POST.get("hotel_fee", None)  # 住宿费
        cosmetic_fee = request.POST.get("cosmetic_fee", None)  # 护理依赖期限

        nurse_one = request.POST.get("nurse_one", None)  # 护理人1工作状况
        nurse_one_wage = request.POST.get("nurse_one_wage", None)  # 日工资
        nurse_one_days = request.POST.get("nurse_one_days", None)  # 护理天数

        nurse_two = request.POST.get("nurse_two", None)  # 护理人2工作状况
        nurse_two_wage = request.POST.get("nurse_two_wage", None)  # 日工资
        nurse_two_days = request.POST.get("nurse_two_days", None)  # 护理天数
        hospital = {
            "enter_time": enter_time,
            "leave_time": leave_time,
            "hospital_day": hospital_day,
            "hospital_costs": hospital_costs,
            "rest_day": rest_day,
            "nutrition": nutrition,
            "device_cost": device_cost,
            "device_period": device_period,
            "car_fee": car_fee,
            "hotel_fee": hotel_fee,
            "cosmetic_fee": cosmetic_fee,
            "nurse_one": nurse_one,
            "nurse_one_wage": nurse_one_wage,
            "nurse_one_days": nurse_one_days,
            "nurse_two": nurse_two,
            "nurse_two_wage": nurse_two_wage,
            "nurse_two_days": nurse_two_days,
        }
        calculator = request.session[settings.CALCULATOR_SESSION_KEY]
        calculator["hospital"] = hospital
        request.session[settings.CALCULATOR_SESSION_KEY] = calculator
        return redirect(reverse("calculator:appraise-index"))


class AppraiseCalcView(View):
    """鉴定信息计算"""
    def get(self, request, *args, **kwargs):
        DisabilityFormSet = formset_factory(DisabilityForm, extra=1)
        disability_formset = DisabilityFormSet()
        disability_type = dict(DISABILITY_TYPE)
        context = {
            "disability_formset": disability_formset,
            "disability_type": disability_type,
        }
        return render(request, template_name="calculator/appraise.html", context=context)

    def post(self, request, *args, **kwargs):
        fixed_date = request.POST.get("fixed_date", None)  # 定残日期
        nutrition_duration = request.POST.get("nutrition_duration", None)  # 营养期限
        delay_duration = request.POST.get("delay_duration", None)  # 误工期限
        nurse_duration = request.POST.get("nurse_duration", None)  # 护理期限
        nurse_persons = request.POST.get("nurse_persons", None)  # 护理人数
        late_treat_fee = request.POST.get("late_treat_fee", None)  # 鉴定后期治疗费
        nurse_depend_level = request.POST.get("nurse_depend_level", None)  # 护理依赖等级
        nurse_depend_duration = request.POST.get("nurse_depend_duration", None)  # 护理依赖期限

        appraise_fee = request.POST.get("appraise_fee", None)  # 鉴定费
        top_disability = request.POST.get("top_disability", None)  # 顶级伤残

        DisabilityFormSet = formset_factory(DisabilityForm, extra=0)
        disability_formset = DisabilityFormSet(request.POST)

        sec_disability = None
        if disability_formset.is_valid():
            disability_list = disability_formset.cleaned_data

            disa_list = [item["name"] for item in disability_list if item]
            print(disa_list)
            sec_disability = disa_list

        disability = {
            "fixed_date": fixed_date,
            "nutrition_duration": nutrition_duration,
            "delay_duration": delay_duration,
            "nurse_duration": nurse_duration,
            "nurse_persons": nurse_persons,
            "late_treat_fee": late_treat_fee,
            "nurse_depend_level": nurse_depend_level,
            "nurse_depend_duration": nurse_depend_duration,
            "appraise_fee": appraise_fee,
            "top_disability": top_disability,
            "sec_disability": sec_disability if sec_disability else [],
        }

        calculator = request.session[settings.CALCULATOR_SESSION_KEY]
        calculator["disability"] = disability
        request.session[settings.CALCULATOR_SESSION_KEY] = calculator
        return redirect(reverse("calculator:relation-index"))


class RelationCalcView(View):
    """亲属信息计算"""
    def get(self, request, *args, **kwargs):
        form = CalculatorUserForm()
        supported_formset = SupportedFormSet()
        relation_formset = RelationFormSet()

        context = {
            "form": form,
            "relation_formset": relation_formset,
            "supported_formset": supported_formset
        }
        return render(request, template_name="calculator/relationship.html", context=context)

    def post(self, request, *args, **kwargs):

        form = CalculatorUserForm(request.POST)
        supported_formset = SupportedFormSet(request.POST)
        relation_formset = RelationFormSet(request.POST)
        if form.is_valid() and supported_formset.is_valid() and relation_formset.is_valid():
            supported_list = supported_formset.cleaned_data
            print(supported_list)
            for supported in supported_list:
                if supported:
                    supported.pop("user")
                    supported.pop("DELETE")

            relation_list = relation_formset.cleaned_data
            for relation in relation_list:
                if relation:
                    relation.pop("user")
                    relation.pop("DELETE")

            calculator = request.session[settings.CALCULATOR_SESSION_KEY]
            calculator["supported"] = supported_list
            calculator["relation"] = relation_list
            request.session[settings.CALCULATOR_SESSION_KEY] = calculator
        return redirect(reverse("calculator:calc-result"))


class CalculatorResultView(View):
    """计算结果"""
    def get(self, request, *args, **kwargs):
        calculator = request.session.get(settings.CALCULATOR_SESSION_KEY)
        print(calculator)
        spirit_fee = float(calculator["spirit_fee"]) if calculator["spirit_fee"] else 0     # 精神抚慰金
        other_fee = float(calculator["other_fee"]) if calculator["other_fee"] else 0        # 其他费用

        hospital_fee = float(calculator["hospital"]["hospital_costs"]) if calculator["hospital"]["hospital_costs"] else 0
        car_fee = float(calculator["hospital"]["car_fee"]) if calculator["hospital"]["car_fee"] else 0    # 交通费
        hotel_fee = float(calculator["hospital"]["hotel_fee"]) if calculator["hospital"]["hotel_fee"] else 0     # 住宿费
        appraise_fee = float(calculator["disability"]["appraise_fee"]) if calculator["disability"]["appraise_fee"] else 0   # 鉴定费
        device_cost = float(calculator["hospital"]["device_cost"]) if calculator["hospital"]["device_cost"] else 0    # 伤残辅助器具费
        funeral_expense = float(calculator["funeral_expense"]) if calculator["funeral_expense"] else 0
        cosmetic_expense = float(calculator["hospital"]["cosmetic_fee"]) if calculator["hospital"]["cosmetic_fee"] else 0
        delay_fee = self.delay_fee(request, calculator=calculator)  # 误工费
        nurse_fee = self.nurse_fee(request, calculator=calculator)  # 护理费
        food_allowance = self.food_allowance(request, calculator=calculator)  # 住院伙食补助费
        nurse_denpendence = self.nurse_denpendence(request, calculator=calculator)  # 护理依赖费
        nutrition_fee = self.nutrition_fee(request, calculator=calculator)  # 营养费
        dead_compensation_fee = self.dead_compensation_fee(request, calculator=calculator)  # 死亡赔偿金
        disability_fee = self.disability_fee(request, calculator=calculator)    # 伤残赔偿金
        supported_living_expense = self.supported_living_expense(request, calculator=calculator)    # 生活费

        totals_money = [
            hospital_fee, car_fee, hotel_fee, appraise_fee, spirit_fee, other_fee,
            device_cost, funeral_expense, cosmetic_expense,
            delay_fee.get("value", 0), nurse_fee.get("value", 0),
            food_allowance.get("value", 0), nurse_denpendence.get("value", 0),
            nutrition_fee.get("value", 0), dead_compensation_fee.get("value", 0),
            disability_fee.get("value", 0), supported_living_expense.get("value", 0)
        ]
        print(totals_money)
        totals_fee = sum(totals_money)
        return render(request, template_name="calculator/calculator_results.html", context=locals())

    def calc_day_wage(self, request, *args, **kwargs):
        """计算日工资"""
        calculator = kwargs.get("calculator")
        fix_income = calculator["fix_income"]
        if not fix_income:
            return 0

        if fix_income == "1":       # 有固定收入
            fix_income_money = calculator["fix_income_money"] if calculator["fix_income_money"] else 0
            return float(fix_income_money)
        else:
            prove_income = calculator["prove_income"]
            if prove_income:
                return float(prove_income)
            else:
                industry_wage = calculator["industry_wage"] if calculator["industry_wage"] else "0"
                return float(industry_wage)

    def calc_delay_day(self, request, *args, **kwargs):
        """计算误工时间"""
        calculator = kwargs.get("calculator")
        fixed_date = calculator["disability"]["fixed_date"]
        if fixed_date:
            enter_time = calculator["hospital"]["enter_time"]
            if enter_time:
                delay_duration = calculator["disability"]["delay_duration"] if calculator["disability"]["delay_duration"] else "0"
                d_fixed_date = datetime.datetime.strptime(fixed_date, "%Y-%m-%d").date()
                d_enter_date = datetime.datetime.strptime(enter_time, "%Y-%m-%d").date()
                day_diff = (d_fixed_date - d_enter_date).days
                return day_diff + int(delay_duration)
            else:
                return 0
        else:
            enter_time = calculator["hospital"]["enter_time"]
            leave_time = calculator["hospital"]["leave_time"]
            if enter_time and leave_time:
                rest_day = calculator["hospital"]["rest_day"] if calculator["hospital"]["rest_day"] else "0"
                delay_duration = calculator["disability"]["delay_duration"] if calculator["disability"]["delay_duration"] else "0"
                d_enter_time = datetime.datetime.strptime(enter_time, "%Y-%m-%d").date()
                d_leave_time = datetime.datetime.strptime(leave_time, "%Y-%m-%d").date()
                day_diff = (d_leave_time - d_enter_time).days + 1
                return day_diff + int(rest_day) + int(delay_duration)
            else:
                return 0

    def delay_fee(self, request, *args, **kwargs):
        """误工费"""
        calculator = kwargs.get("calculator")
        day_wage = self.calc_day_wage(request, calculator=calculator)
        delay_days = self.calc_delay_day(request, calculator=calculator)
        value = day_wage * delay_days
        formats = "{} X {} = {}".format(day_wage, delay_days, value)
        delay_fee = {
            "value": value,
            "formats": formats,
        }
        return delay_fee

    def nurse_fee(self, request, *args, **kwargs):
        """护理费用"""
        calculator = kwargs.get("calculator")
        nurse_one_wage = calculator["hospital"]["nurse_one_wage"]
        nurse_one_wage = float(nurse_one_wage) if nurse_one_wage else 0

        nurse_one_days = calculator["hospital"]["nurse_one_days"]
        nurse_one_days = float(nurse_one_days) if nurse_one_days else 0

        nurse_two_wage = calculator["hospital"]["nurse_two_wage"]
        nurse_two_wage = float(nurse_two_wage) if nurse_two_wage else 0

        nurse_two_days = calculator["hospital"]["nurse_two_days"]
        nurse_two_days = float(nurse_two_days) if nurse_two_days else 0

        value =nurse_one_wage * nurse_one_days + nurse_two_wage * nurse_two_days

        if nurse_two_wage > 0 and nurse_two_days > 0:
            formats = "{} X {} + {} X {} = {}".format(nurse_one_wage, nurse_one_days, nurse_two_wage, nurse_two_days, value)
        else:
            formats = "{} X {} = {}".format(nurse_one_wage, nurse_one_days, value)

        nurse_fee = {
            "value": value,
            "formats": formats
        }
        return nurse_fee

    def food_allowance(self, request, *args, **kwargs):
        """伙食补助"""
        calculator = kwargs.get("calculator")
        # 读取伙食补助标准 id = 7
        province = calculator.get("province", None)
        res_income_expend = ResIncomeExpend.objects.filter(inc_exp_item_id=7, province_id=province).order_by("-years").first()
        if res_income_expend:
            hospital_day = calculator["hospital"]["hospital_day"]
            hospital_day = float(hospital_day) if hospital_day else 0
            value = float(res_income_expend.total_money) * hospital_day
            formats = "{} X {} = {}".format(res_income_expend.total_money, hospital_day, value)
        else:
            value = 0
            formats = "无伙食补助标准"

        food_allowance = {
            "value": value,
            "formats": formats,
        }
        return food_allowance

    def nurse_denpendence(self, request, *args, **kwargs):
        """护理依赖费"""
        calculator = kwargs.get("calculator")
        # 读取护理依赖费标准 id = 5(城镇单位在岗职工平均工资)
        province = calculator.get("province", None)
        court_province = calculator.get("court_province", None)
        res_income_expend = ResIncomeExpend.objects.filter(inc_exp_item_id=5, province_id=province).order_by("-years").first()
        court_res_income_expend = ResIncomeExpend.objects.filter(inc_exp_item_id=5, province_id=court_province).order_by("-years").first()

        if res_income_expend and court_res_income_expend:
            total_money = res_income_expend.total_money if res_income_expend.total_money >= court_res_income_expend.total_money else court_res_income_expend.total_money
            nurse_depend_duration = calculator["disability"]["nurse_depend_duration"]
            nurse_depend_duration = int(nurse_depend_duration) if nurse_depend_duration else 0

            nurse_depend_level = calculator["disability"]["nurse_depend_level"]
            nurse_depend_level = int(nurse_depend_level) if nurse_depend_level else 0
            value = total_money / 365 * nurse_depend_level / 100 * nurse_depend_duration
            value = float(value.quantize(decimal.Decimal("0.01")))
            formats = "({} / 365) X ({}/100) X {} = {}".format(total_money, nurse_depend_level, nurse_depend_duration, value)
        else:
            value = 0
            formats = "无护理依赖标准"

        nurse_denpendence = {
            "value": value,
            "formats": formats,
        }
        return nurse_denpendence

    def nutrition_fee(self, request, *args, **kwargs):
        """营养费"""
        calculator = kwargs.get("calculator")
        nutrition = calculator["hospital"]["nutrition"]
        if nutrition == "1":
            hospital_day = calculator["hospital"]["hospital_day"]
            hospital_day = int(hospital_day) if hospital_day else 0
        else:
            hospital_day = 0

        nutrition_duration = calculator["disability"]["nutrition_duration"]
        nutrition_duration = int(nutrition_duration) if nutrition_duration else 0

        # nutrition_wage = ResIncomeExpend.objects.filter()

        value = (hospital_day + nutrition_duration) * NUTRITION_WAGE
        formats = "({} + {}) X {} = {}".format(hospital_day, nutrition_duration, NUTRITION_WAGE, value)

        nutrition_fee = {
            "value": value,
            "formats": formats,
        }
        return nutrition_fee

    def compensation_years(self, age):
        """赔偿年限"""
        if age <= 60:
            return 20
        elif 60 < age <= 75:
            return 20 - (age - 60)
        else:
            return 5

    def compensation_wage(self, house_type, province, court_province):
        """赔偿标准"""
        last_year = datetime.datetime.now().year - 1
        if house_type == "1":   # 城镇
            res_income_expend = ResIncomeExpend.objects.filter(inc_exp_item_id=1, province_id=province,
                                                               years=last_year).first()
            court_res_income_expend = ResIncomeExpend.objects.filter(inc_exp_item_id=1, province_id=court_province,
                                                                     years=last_year).first()
        elif house_type == "2":
            res_income_expend = ResIncomeExpend.objects.filter(inc_exp_item_id=2, province_id=province,
                                                               years=last_year).first()
            court_res_income_expend = ResIncomeExpend.objects.filter(inc_exp_item_id=2, province_id=court_province,
                                                                     years=last_year).first()
        else:
            return -1

        if res_income_expend and court_res_income_expend:
            total_money = res_income_expend.total_money if res_income_expend.total_money >= court_res_income_expend.total_money else court_res_income_expend.total_money
            return float(total_money)
        else:
            return -1

    def dead_compensation_fee(self, request, *args, **kwargs):
        """死亡赔偿金"""
        calculator = kwargs.get("calculator")
        dead = calculator.get("dead")
        if dead and dead == "1":
            age = calculator.get("age", 0)
            province = calculator.get("province")
            court_province = calculator.get("court_province")
            house_type = calculator.get("house_type")
            compen_years = self.compensation_years(int(age))
            compen_wage = self.compensation_wage(house_type, province, court_province)

            if compen_wage != -1:
                value = compen_wage * compen_years
                formats = "{} X {} = {}".format(compen_wage, compen_years, value)
            else:
                value = 0
                formats = "无法正确读取居民人均可支配收入"

            dead_compensation_fee = {
                "value": value,
                "formats": formats,
            }
        else:
            dead_compensation_fee = {
                "value": 0,
                "formats": "",
            }
        return dead_compensation_fee

    def disability_fee(self, request, *args, **kwargs):
        """伤残赔偿金"""
        calculator = kwargs.get("calculator")
        dead = calculator.get("dead")
        disability_fee = {
            "value": 0,
            "formats": "",
        }
        if not dead or dead == "0":
            age = calculator.get("age", 0)
            province = calculator.get("province")
            court_province = calculator.get("court_province")
            house_type = calculator.get("house_type")
            compen_years = self.compensation_years(int(age))
            compen_wage = self.compensation_wage(house_type, province, court_province)
            if compen_wage == -1:
                disability_fee["value"] = 0
                disability_fee["formats"] = "无法正确读取居民人均可支配收入"
            else:
                top_disability = calculator["disability"]["top_disability"]
                top_disability = int(top_disability) if top_disability else 0
                sec_disability = calculator["disability"]["sec_disability"]

                sec_disability_sum = 0
                if sec_disability:
                    sec_disability_sum = sum([int(item) for item in sec_disability])

                disability_factors = top_disability + sec_disability_sum
                value = compen_wage * compen_years * disability_factors/100
                formats = "{} X {} X {}/100".format(compen_wage, compen_years, disability_factors)
                disability_fee["value"] = value
                disability_fee["formats"] = formats

        return disability_fee

    def per_consumption_expend(self, house_type, province, court_province):
        """居民人均消费支出"""
        last_year = datetime.datetime.now().year - 1
        if house_type == "1":  # 城镇
            res_income_expend = ResIncomeExpend.objects.filter(inc_exp_item_id=3, province_id=province,
                                                               years=last_year).first()
            court_res_income_expend = ResIncomeExpend.objects.filter(inc_exp_item_id=3, province_id=court_province,
                                                                     years=last_year).first()
        elif house_type == "2":
            res_income_expend = ResIncomeExpend.objects.filter(inc_exp_item_id=4, province_id=province,
                                                               years=last_year).first()
            court_res_income_expend = ResIncomeExpend.objects.filter(inc_exp_item_id=4, province_id=court_province,
                                                                     years=last_year).first()
        else:
            return -1

        if res_income_expend and court_res_income_expend:
            return res_income_expend.total_money if res_income_expend.total_money >= court_res_income_expend.total_money else court_res_income_expend.total_money
        else:
            return -1

    def supported_living_expense(self, request, *args, **kwargs):
        """被抚(扶)养人生活费"""
        calculator = kwargs.get("calculator")
        relations = calculator.get("relation")
        supported = calculator.get("supported")
        province = calculator.get("province")
        court_province = calculator.get("court_province")
        house_type = calculator.get("house_type")
        per_consumption_exp = self.per_consumption_expend(house_type, province, court_province)

        living_expense = {
            "value": 0,
            "formats": "无法正确读取居民人均消费支出"
        }
        if per_consumption_exp == -1:
            return living_expense

        # 配偶情况
        PARTNER = 5  # 配偶
        BROTHOR = 6  # 兄弟姐妹
        join_partner = 1
        broth_sist_counts = 1
        for relation in relations:
            if not relation:
                continue
            # 配偶
            if relation["relation_type"] == PARTNER:
                if relation["is_income"] == 0 or relation["action_ability"] == 1 or relation["relation_age"] >= 60:
                    pass
                else:
                    join_partner += 1

            if relation["relation_type"] == BROTHOR:
                if relation["is_income"] == 1 and relation["action_ability"] == 0 and 60 > relation["relation_age"] >= 18:
                    broth_sist_counts += 1

        # 计算赔偿年限
        expense_day = []
        for s in supported:
            if not s:
                continue
            if s["relation_type"] == 3:          # 子女
                if s["action_ability"] == 1:     # 残障
                    expense_day.append((MAX_PAY_YEARS, s["relation_type"]))
                else:                           # 无残障
                    if s["relation_age"] < 18:
                        expense_day.append((18 - s["relation_age"], s["relation_type"]))
            elif s["relation_type"] == 5:       # 配偶
                if s["action_ability"] == 1:
                    if s["relation_age"] < 60:
                        expense_day.append((MAX_PAY_YEARS, s["relation_type"]))
                    else:
                        expense_day.append((MAX_YEARS - s["relation_age"], s["relation_type"]))
            elif s["relation_type"] == 1 or s["relation_type"] == 2:      # 父母
                if s["relation_age"] < 60 and (s["action_ability"] == 1 or s["is_income"] == 0):    # 未到60有残障或无生活来源
                    expense_day.append((MAX_PAY_YEARS, s["relation_type"]))

                elif s["relation_age"] >= 60:
                    expense_day.append((MAX_YEARS - s["relation_age"], s["relation_type"]))

        expense_day.sort()
        list_expense = []
        for i in range(1, len(expense_day)):
            if i == 1:
                list_expense.append((expense_day[i - 1][0], expense_day[i - 1][1]))
                list_expense.append((expense_day[i][0] - expense_day[i - 1][0], expense_day[i][1]))
            else:
                list_expense.append((expense_day[i][0] - expense_day[i - 1][0], expense_day[i][1]))

        list_expense_ex = []
        for i in range(0, len(list_expense)):
            dict_expense = {
                "years": list_expense[i][0],
                "persons": []
            }
            for j in range(i, len(list_expense)):
                dict_expense["persons"].append(list_expense[j][1])

            list_expense_ex.append(dict_expense)

        list_expense_result = [item for item in list_expense_ex if item["years"] > 0]


        list_total_expense = []
        for item in list_expense_result:
            years = item["years"]
            phase_expense = []
            persons = item["persons"]
            max_expense = per_consumption_exp * years
            for ptype in persons:
                if ptype == 3:    # 子女
                    expense = per_consumption_exp * years / join_partner
                    phase_expense.append(expense)
                elif ptype == 1 or ptype == 2:    # 父母
                    expense = per_consumption_exp * years / broth_sist_counts
                    phase_expense.append(expense)

            phase_expense_sum = sum(phase_expense)
            phase_expense_sum = phase_expense_sum if phase_expense_sum <= max_expense else max_expense
            list_total_expense.append(phase_expense_sum)

        total_expense_sum = sum(list_total_expense)
        formats = [str(item) for item in list_total_expense]
        living_expense["value"] = total_expense_sum
        living_expense["formats"] = "{} = {}".format(" + ".join(formats), total_expense_sum)

        return living_expense


