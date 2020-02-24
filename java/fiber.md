- Maybe will be supported in JAVA 14
- When create thread, it needs to call OS kernel which takes long time and consume more resource.
- When create fiber, it will be created via user-mode.
- Why it is slow for system kernel call?
  - app发出0x80中断或调用sysenter原语
  - os进入内核态
  - 在中断向量表中查找处理例程
  - 保存硬件现场CS IP等寄存器值
  - 执行中断例程system call
    - 根据参数和编号寻找对应例程
    - 执行并返回
  - 恢复现场
  - 返回用户态
  - app继续执行


