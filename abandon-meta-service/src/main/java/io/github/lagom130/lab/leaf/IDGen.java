package io.github.lagom130.lab.leaf;


import io.github.lagom130.lab.leaf.common.Result;

public interface IDGen {
    Result get(String key);
    boolean init();
}
