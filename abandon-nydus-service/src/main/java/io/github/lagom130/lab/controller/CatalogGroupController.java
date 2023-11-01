package io.github.lagom130.lab.controller;

import io.github.lagom130.lab.client.MetaClient;
import io.github.lagom130.lab.dto.CatalogGroupDTO;
import io.github.lagom130.lab.entity.CatalogGroup;
import io.github.lagom130.lab.enums.CatalogTypeEnum;
import io.github.lagom130.lab.globalResponse.Result;
import io.github.lagom130.lab.service.ICatalogGroupService;
import io.github.lagom130.lab.util.SnowFlakeUtil;
import io.github.lagom130.lab.vo.CatalogGroupNodeVO;
import jakarta.annotation.Resource;
import org.springframework.boot.context.properties.bind.DefaultValue;
import org.springframework.util.NumberUtils;
import org.springframework.web.bind.annotation.*;
import org.springframework.stereotype.Controller;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * <p>
 *  前端控制器
 * </p>
 *
 * @author lagom
 * @since 2023-10-29
 */
@Controller
@RequestMapping("/api/catalogGroup")
public class CatalogGroupController {
    @Resource
    private ICatalogGroupService catalogGroupService;
    @Resource
    private MetaClient metaClient;

    @PostMapping("")
    public Result<Long> addOne(@RequestBody CatalogGroupDTO dto) {
        return new Result<Long>().success(catalogGroupService.addOne(dto));
    }

    @PutMapping("")
    public Result<Void> updateOne(@PathVariable("id") Long id, @RequestBody CatalogGroupDTO dto) {
        catalogGroupService.updateOne(id, dto);
        return new Result<Void>().success();
    }

    @DeleteMapping("/{id}")
    public Result<Void> deleteOne(@PathVariable("id") Long id) {
        catalogGroupService.deleteOne(id);
        return new Result<Void>().success();
    }

    @GetMapping("/{id}")
    public Result<CatalogGroup> getOne(@PathVariable("id") String idStr) {
        Long id = NumberUtils.parseNumber(idStr, Long.class);
        if(id<0 || id> SnowFlakeUtil.getCurrentMax()) {
            return new Result<CatalogGroup>().success(null);
        }
        return new Result<CatalogGroup>().success(catalogGroupService.getOne(id));
    }

    @GetMapping("/tree")
    public Result<List<CatalogGroupNodeVO>> getTree(@RequestParam("noCaches") @DefaultValue("false") String noCaches) {
        return new Result<List<CatalogGroupNodeVO>>().success(catalogGroupService.getTree(Boolean.parseBoolean(noCaches)));
    }

    @GetMapping("/fake")
    public void fake() {
        // 创建一个HashMap用于存储省份信息
        Map<String, String> provinceMap = new HashMap<>();
        // 添加省份信息到HashMap中
        provinceMap.put("11", "北京市");
        provinceMap.put("12", "天津市");
        provinceMap.put("13", "河北省");
        provinceMap.put("14", "山西省");
        provinceMap.put("15", "内蒙古自治区");
        provinceMap.put("21", "辽宁省");
        provinceMap.put("22", "吉林省");
        provinceMap.put("23", "黑龙江省");
        provinceMap.put("31", "上海市");
        provinceMap.put("32", "江苏省");
        provinceMap.put("33", "浙江省");
        provinceMap.put("34", "安徽省");
        provinceMap.put("35", "福建省");
        provinceMap.put("36", "江西省");
        provinceMap.put("37", "山东省");
        provinceMap.put("41", "河南省");
        provinceMap.put("42", "湖北省");
        provinceMap.put("43", "湖南省");
        provinceMap.put("44", "广东省");
        provinceMap.put("45", "广西壮族自治区");
        provinceMap.put("46", "海南省");
        provinceMap.put("50", "重庆市");
        provinceMap.put("51", "四川省");
        provinceMap.put("52", "贵州省");
        provinceMap.put("53", "云南省");
        provinceMap.put("54", "西藏自治区");
        provinceMap.put("61", "陕西省");
        provinceMap.put("62", "甘肃省");
        provinceMap.put("63", "青海省");
        provinceMap.put("64", "宁夏回族自治区");
        provinceMap.put("65", "新疆维吾尔自治区");
        provinceMap.put("71", "香港");
        provinceMap.put("72", "澳门");
        provinceMap.put("73", "台湾");
        List<String> tiangang = new ArrayList<>();
        tiangang.add("天机");
        tiangang.add("天枢");
        tiangang.add("天权");
        tiangang.add("天英");
        tiangang.add("天勇");
        tiangang.add("天雄");
        tiangang.add("天柱");
        tiangang.add("天任");
        tiangang.add("天顺");
        tiangang.add("天虚");
        tiangang.add("天喜");
        tiangang.add("天闲");
        tiangang.add("天寿");
        tiangang.add("天祚");
        tiangang.add("天藏");
        tiangang.add("天孤");
        tiangang.add("天强");
        tiangang.add("天危");
        tiangang.add("天持");
        tiangang.add("天星");
        tiangang.add("天尔");
        tiangang.add("天明");
        tiangang.add("天梦");
        tiangang.add("天帝");
        tiangang.add("天贵");
        tiangang.add("天克");
        tiangang.add("天伤");
        tiangang.add("天官");
        tiangang.add("天刑");
        tiangang.add("天变");
        tiangang.add("天威");
        List<String> solarTerms = new ArrayList<>();
        solarTerms.add("春分");
        solarTerms.add("清明");
        solarTerms.add("谷雨");
        solarTerms.add("立夏");
        solarTerms.add("小满");
        solarTerms.add("芒种");
        solarTerms.add("夏至");
        solarTerms.add("小暑");
        solarTerms.add("大暑");
        solarTerms.add("立秋");
        solarTerms.add("处暑");
        solarTerms.add("白露");
        solarTerms.add("秋分");
        solarTerms.add("寒露");
        solarTerms.add("霜降");
        solarTerms.add("立冬");
        solarTerms.add("小雪");
        solarTerms.add("大雪");
        solarTerms.add("冬至");
        solarTerms.add("小寒");
        solarTerms.add("大寒");
        List<String> constellations = new ArrayList<>();
        constellations.add("白羊");
        constellations.add("金牛");
        constellations.add("双子");
        constellations.add("巨蟹");
        constellations.add("狮子");
        constellations.add("处女");
        constellations.add("天秤");
        constellations.add("天蝎");
        constellations.add("射手");
        constellations.add("摩羯");
        constellations.add("水瓶");
        constellations.add("双鱼");
        List<String> luohans = new ArrayList<>();

        luohans.add("清净");
        luohans.add("总持");
        luohans.add("寂静");
        luohans.add("迦叶");
        luohans.add("憎禅");
        luohans.add("阿难");
        luohans.add("拘留孙");
        luohans.add("彌勒");
        luohans.add("藥王");
        luohans.add("得道");
        luohans.add("栖禅");
        luohans.add("持国");
        luohans.add("护国");
        luohans.add("降魔");
        luohans.add("除盖障");
        luohans.add("迦葉");
        luohans.add("般若多罗");
        List<String> stratagems = new ArrayList<>();

        stratagems.add("瞒天过海");
        stratagems.add("围魏救赵");
        stratagems.add("借刀杀人");
        stratagems.add("待而后动");
        stratagems.add("趁火打窃");
        stratagems.add("声东击西");
        stratagems.add("无中生有");
        stratagems.add("暗渡陈仓");
        stratagems.add("隔岸观火");
        stratagems.add("笑里藏刀");
        stratagems.add("李代桃僵");
        stratagems.add("顺手牵羊");
        stratagems.add("打草惊蛇");
        stratagems.add("指桑骂槐");
        stratagems.add("假途伐虢");
        stratagems.add("上屋抽梯");
        stratagems.add("故意壶漏");
        stratagems.add("欲擒故纵");
        stratagems.add("抛砖引玉");
        stratagems.add("疑火令");
        stratagems.add("借尸还魂");
        stratagems.add("调虎离山");
        stratagems.add("开门诱盗");
        stratagems.add("远交近攻");
        stratagems.add("避实击虚");
        stratagems.add("假痴不癫");
        stratagems.add("上借下还");
        stratagems.add("壮士断腕");
        stratagems.add("美人计");
        stratagems.add("反客为主");
        stratagems.add("以逸待劳");
        stratagems.add("趋炎附势");
        stratagems.add("欺夫惑妇");
        stratagems.add("双重间谍");
        stratagems.add("欲擒故纵");
        stratagems.add("声东击西");
        List<String> hours = new ArrayList<>();

        hours.add("子"); // 23:00-01:00
        hours.add("丑"); // 01:00-03:00
        hours.add("寅"); // 03:00-05:00
        hours.add("卯"); // 05:00-07:00
        hours.add("辰");
        hours.add("巳");
        hours.add("午");
        hours.add("未");
        hours.add("申");
        hours.add("酉");
        hours.add("戌");
        hours.add("亥");
        provinceMap.entrySet().parallelStream().forEach(entry -> {
            String provinceName = entry.getValue();
            CatalogGroupDTO province = new CatalogGroupDTO();
            province.setName(provinceName);
            province.setCode(entry.getKey());
            province.setPid(null);
            Long provinceId = catalogGroupService.addOne(province);
            List<CatalogGroup> batch = new ArrayList<>();
            for (int j = 0; tiangang.size() < 60; j++) {
                String cityName = tiangang.get(j);
                CatalogGroup city = new CatalogGroup();
                city.setId(metaClient.getSnowflakeId());
                city.setName(cityName+"市");
                city.setCode(province.getCode()+(j<10?"0"+j:""+j));
                city.setPid(provinceId);
                city.setPids(""+provinceId);
                batch.add(city);
                for (int a = 0; a < solarTerms.size(); a++) {
                    String areaName = solarTerms.get(a);
                    CatalogGroup area = new CatalogGroup();
                    area.setId(metaClient.getSnowflakeId());
                    area.setName(areaName+"区");
                    area.setCode(city.getCode()+(a<10?"0"+a:""+a));
                    String areaCode = area.getCode();
                    area.setPid(city.getId());
                    area.setPids(city.getPids() + "," + city.getId());
                    area.setCatalogType(CatalogTypeEnum.DEPT);
                    batch.add(area);
                    for (int b = 0; b < constellations.size(); b++) {
                        String screetName = constellations.get(b);
                        CatalogGroup street = new CatalogGroup();
                        street.setId(metaClient.getSnowflakeId());
                        street.setName(screetName+"街道");
                        street.setCode(area.getCode()+(b<10?"0"+b:""+b));
                        street.setPid(area.getId());
                        street.setPids(area.getPids() + "," + area.getId());
                        street.setRegionCode(areaCode);
                        street.setCatalogType(CatalogTypeEnum.DEPT);
                        batch.add(street);
                        for (int c = 0; c < luohans.size(); c++) {
                            String deptName = luohans.get(c);
                            CatalogGroup dept = new CatalogGroup();
                            dept.setId(metaClient.getSnowflakeId());
                            dept.setName(deptName+"局");
                            dept.setCode(street.getCode()+"01"+(c<10?"0"+c:""+c));
                            dept.setPid(street.getId());
                            dept.setPids(street.getPids() + "," + street.getId());
                            dept.setRegionCode(areaCode);
                            dept.setCatalogType(CatalogTypeEnum.DEPT);
                            batch.add(dept);
                        }
                    }
                    for (int d = 0; d < stratagems.size(); d++) {
                        String themeName = stratagems.get(d);
                        CatalogGroup theme = new CatalogGroup();
                        theme.setId(metaClient.getSnowflakeId());
                        theme.setName(themeName);
                        theme.setCode(area.getCode()+"03"+(d<10?"0"+d:""+d));
                        theme.setPid(area.getId());
                        theme.setPids(area.getPids() + "," + area.getId());
                        theme.setRegionCode(areaCode);
                        theme.setCatalogType(CatalogTypeEnum.THEME);
                        batch.add(theme);
                    }
                    for (int d = 0; d < hours.size(); d++) {
                        String themeName = hours.get(d);
                        CatalogGroup theme = new CatalogGroup();
                        theme.setId(metaClient.getSnowflakeId());
                        theme.setName(themeName);
                        theme.setCode(area.getCode()+"02"+(d<10?"0"+d:""+d));
                        theme.setPid(area.getId());
                        theme.setPids(area.getPids() + "," + area.getId());
                        theme.setRegionCode(areaCode);
                        theme.setCatalogType(CatalogTypeEnum.BASIC);
                        batch.add(theme);
                    }
                }

            }
            catalogGroupService.saveBatch(batch);
        });
    }
}
