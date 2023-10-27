package io.github.lagom130.lab.util;

import io.github.lagom130.lab.globalResponse.BizException;

/**
 * @author lujc
 * @date 2023/10/25.
 */
public class GeneSnowFlakeUtil {

    // 起始时间戳
    private final static long START_STMP = 1696089600000L;

    // 每部分的位数
    private long GENE_BIT=0; // 基因片段占位数，默认0
    private final static long SEQUENCE_BIT = 12; // 序列号占用位数
    private long WORK_ID_BIT = 10; // workid占用位数，默认10，由基于片段决定


    // 每部分最大值
    private long MAX_WORK_ID_NUM;
    private long MAX_SEQUENCE = -1L ^ (-1L << SEQUENCE_BIT);

    // 每部分向左的位移
    private long SEQUENCE_LEFT = GENE_BIT;
    private long WORK_ID_LEFT = SEQUENCE_BIT +SEQUENCE_LEFT;
    private long TIMESTMP_LEFT = WORK_ID_LEFT + WORK_ID_BIT;

    private long workId; // 组件id
    private long sequence = 0L; // 序列号
    private long lastStmp = -1L; // 上次的时间戳

    private int fragment = 0;

    public GeneSnowFlakeUtil(long workId, int fragment) {
        if(fragment%2 != 0) {
            throw new IllegalArgumentException("基因雪花算法创建失败，分片数应能被2整除");
        }
        this.fragment = fragment;
        this.GENE_BIT = Integer.toBinaryString(fragment).length();
        this.WORK_ID_BIT = 10-this.GENE_BIT;
        this.MAX_WORK_ID_NUM = -1L ^ (-1L << this.WORK_ID_BIT);
        this.SEQUENCE_LEFT = this.GENE_BIT;
        this.WORK_ID_LEFT = this.SEQUENCE_BIT +SEQUENCE_LEFT;
        this.TIMESTMP_LEFT = this.WORK_ID_LEFT + WORK_ID_BIT;
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
                | sequence<< SEQUENCE_LEFT // 序列号部分
                | geneticSource%fragment;
    }


    // 获取当前的毫秒数
    private long getNewstmp() {
        return System.currentTimeMillis();
    }

    public static void main(String[] args) {
        int shard = 8;
        long userId = System.currentTimeMillis();
        GeneSnowFlakeUtil generator = new GeneSnowFlakeUtil(0, shard);
        long code = generator.getNextId(userId);
        System.out.println("u: " + userId +" mod "+shard+" = "+ userId%shard);
        System.out.println("c: " + code +" mod "+shard+" = "+ code%shard);
    }
}
