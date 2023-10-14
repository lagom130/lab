package io.github.lagom130.lab.abandon.storage.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.core.conditions.update.LambdaUpdateWrapper;
import com.baomidou.mybatisplus.core.conditions.update.UpdateWrapper;
import io.github.lagom130.lab.abandon.storage.entity.Storage;
import io.github.lagom130.lab.abandon.storage.mapper.StorageMapper;
import io.github.lagom130.lab.abandon.storage.service.IStorageService;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import org.springframework.stereotype.Service;

/**
 * <p>
 *  服务实现类
 * </p>
 *
 * @author lagom
 * @since 2023-10-14
 */
@Service
public class StorageServiceImpl extends ServiceImpl<StorageMapper, Storage> implements IStorageService {

    @Override
    public void deduct(String commodityCode, int count) {
        LambdaQueryWrapper<Storage> queryWrapper = new LambdaQueryWrapper<>();
        queryWrapper.eq(Storage::getCommodityCode, commodityCode);
        Storage storage = this.getOne(queryWrapper);
        if(storage == null) {
            throw new RuntimeException("商品不存在");
        }
        if(storage.getCount()<=0) {
            throw new RuntimeException("库存不足");
        }
        storage.setCount(storage.getCount()-1);
        this.updateById(storage);
    }
}
