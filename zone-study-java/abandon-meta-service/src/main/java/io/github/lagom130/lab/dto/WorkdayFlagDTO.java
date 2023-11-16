package io.github.lagom130.lab.dto;

/**
 * 工作日默认设置
 * @author lujc
 * @date 2023/10/20.
 */
@lombok.Data
public class WorkdayFlagDTO {
    /**
     * 周天
     * 星期几 1~7，
     * 星期一是1，星期日是7
     */
    private int dayOfWeek;
    /**
     * 工作日标识， true为工作日， false为节假日
     */
    private boolean workdayFlag;

}
