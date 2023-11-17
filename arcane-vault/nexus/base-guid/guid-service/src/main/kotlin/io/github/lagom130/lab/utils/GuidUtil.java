package io.github.lagom130.lab.utils;

/**
 * @author lujc
 * @date 2023/10/25.
 */
public class GuidUtil {

    // 起始时间戳
    private final static long START_STMP = 1700000000000L;

    // 每部分的位数
    private final static long GENE_BIT = 6; // 基因片段占位数，默认6,可分32张表
    private final static long SEQUENCE_BIT = 12; // 序列号占用位数
    private final static long WORK_ID_BIT = 4; // workid占用位数，默认4，由基于片段决定


    // 每部分最大值
    private final static long MAX_WORK_ID_NUM = -1L ^ (-1L << WORK_ID_BIT);
    private final static long MAX_SEQUENCE = -1L ^ (-1L << SEQUENCE_BIT);

    // 每部分向左的位移
    private final static long SEQUENCE_LEFT = GENE_BIT;
    private final static long WORK_ID_LEFT = SEQUENCE_BIT + SEQUENCE_LEFT;
    private final static long TIMESTMP_LEFT = WORK_ID_LEFT + WORK_ID_BIT;

    private long workId; // 组件id
    private long sequence = 0L; // 序列号
    private long lastStmp = -1L; // 上次的时间戳

    private final static int fragment = 32;

    public GuidUtil(long workId) {
        this.workId = workId;
    }

    // 产生下一个ID
    public synchronized long getNextId(long geneticSource) {
        long currStmp = getNewstmp();
        // 时钟回拨，用记录的最大时间戳继续生成，透支未来
        if (lastStmp > currStmp) currStmp = lastStmp;
        if (currStmp == lastStmp) {
            // 若在相同毫秒内 序列号自增
            sequence = (sequence + 1) & MAX_SEQUENCE;
            // 同一毫秒的序列数已达到最大，取下一毫秒的序列数，透支未来
            if (sequence == 0L) {
                currStmp++;
            }
        } else {
            // 若在不同毫秒内 则序列号置为0
            sequence = 0L;
        }
        lastStmp = currStmp;
        return (currStmp - START_STMP) << TIMESTMP_LEFT // 时间戳部分
                | workId << WORK_ID_LEFT // 机器id部分
                | sequence << SEQUENCE_LEFT // 序列号部分
                | geneticSource % fragment;
    }

    // 产生下一个ID
    public synchronized long getNextNoGeneId() {
        long currStmp = getNewstmp();
        // 时钟回拨，用记录的最大时间戳继续生成，透支未来
        if (lastStmp > currStmp) currStmp = lastStmp;
        if (currStmp == lastStmp) {
            // 若在相同毫秒内 序列号自增
            sequence = (sequence + 1) & MAX_SEQUENCE;
            // 同一毫秒的序列数已达到最大，取下一毫秒的序列数，透支未来
            if (sequence == 0L) {
                currStmp++;
            }
        } else {
            // 若在不同毫秒内 则序列号置为0
            sequence = 0L;
        }
        lastStmp = currStmp;
        return (currStmp - START_STMP) << TIMESTMP_LEFT // 时间戳部分
                | workId << WORK_ID_LEFT // 机器id部分
                | sequence << SEQUENCE_LEFT; // 序列号部分
    }


    // 获取当前的毫秒数
    private long getNewstmp() {
        return System.currentTimeMillis();
    }


    public static void main(String[] args) {
        System.out.println(Integer.toBinaryString(64).length());
    }
}
