```zsh
conda create -n matlab_python python=3.9
conda activate matlab_python
conda install pyqt opencv numpy matplotlib pyqtchart
```
## 报错
```zsh
(matlab_python) E:\Program Files (x86)\MATLAB\extern\engines\python>python setup.py install
Traceback (most recent call last):
  File "E:\Program Files (x86)\MATLAB\extern\engines\python\setup.py", line 80, in <module>
    setup(
  File "E:\Anaconda\envs\matlab_python\lib\site-packages\setuptools\_distutils\core.py", line 146, in setup
    _setup_distribution = dist = klass(attrs)
  File "E:\Anaconda\envs\matlab_python\lib\site-packages\setuptools\dist.py", line 289, in __init__
    self.metadata.version = self._normalize_version(self.metadata.version)
  File "E:\Anaconda\envs\matlab_python\lib\site-packages\setuptools\dist.py", line 325, in _normalize_version
    normalized = str(Version(version))
  File "E:\Anaconda\envs\matlab_python\lib\site-packages\setuptools\_vendor\packaging\version.py", line 202, in __init__
    raise InvalidVersion(f"Invalid version: '{version}'")
packaging.version.InvalidVersion: Invalid version: 'R2021b'
```
### 解决
```
修改 setup.py
打开 setup.py 文件：
使用文本编辑器打开 E:\Program Files (x86)\MATLAB\extern\engines\python\setup.py 文件。

查找并替换版本号：
找到所有包含 version='R2021b' 的行，并将其替换为 version='2021.2'。确保保存文件。
```

```
pip install .
```
## 

执行脚本
```python
eng.addpath(absolute_matlab_path, nargout=0)
#执行脚本
function1 = 'main'
eng.run(function1, nargout=0)
```
执行函数
```python
eng = matlab.engine.start_matlab()
eng.addpath(absolute_matlab_path, nargout=0)
#调用函数myls
t = eng.myls(4, 2)
```

## Qt multithreading to call MATLAB

在这个类定义中，`run` 方法实际上是由 `QThread` 类的 `start()` 方法自动调用的。具体来说，当你在 `QThread` 对象上调用 `start()` 方法时，Qt 框架会启动一个新的线程，并在这个线程中执行 `run()` 方法的内容。

### 使用 `run` 方法的过程：
1. **定义 `MatlabWorker` 类**：
   - 你在 `__init__` 方法中传递一个函数作为参数，并将其保存为 `self.function`。
   - `run` 方法被定义为调用 `self.function()`，也就是在这个线程中执行你传递的函数。

2. **实例化 `MatlabWorker` 并启动线程**：
   - 当你在主程序中创建 `MatlabWorker` 的实例并调用 `start()` 方法时，Qt 框架会自动调用 `run()` 方法。
   - 这意味着 `self.function()` 会在新线程中执行。

### 示例代码：
```python
def run_pred_1(self):
    self.thread_1 = MatlabWorker(self.pred_1)
    self.thread_1.start()

def run_pred_2(self):
    self.thread_2 = MatlabWorker(self.pred_2)
    self.thread_2.start()
```

在这个示例中，`run_pred_1` 和 `run_pred_2` 方法中分别创建了 `MatlabWorker` 的实例，并传入了 `pred_1` 和 `pred_2` 函数。当你调用 `self.thread_1.start()` 或 `self.thread_2.start()` 时，Qt 会自动在一个新线程中执行 `MatlabWorker` 的 `run()` 方法，进而调用 `pred_1` 或 `pred_2` 函数。

### 总结：
- `run` 方法是由 `QThread` 的 `start()` 方法调用的。
- 在 `MatlabWorker` 类中，`run` 方法执行传入的函数，即你希望在新线程中执行的 MATLAB 相关操作。

这样设计的目的是确保耗时操作（如 MATLAB 函数调用）在独立的线程中执行，不会阻塞主线程，从而保持用户界面的响应性。