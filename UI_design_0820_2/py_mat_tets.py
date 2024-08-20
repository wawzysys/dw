import os
import matlab.engine

current_dir = os.path.dirname(os.path.abspath(__file__))
relative_matlab_path = '../guizhou0714'
absolute_matlab_path = os.path.join(current_dir, relative_matlab_path)
eng = matlab.engine.start_matlab()
eng.addpath(absolute_matlab_path, nargout=0)
#调用函数
# t = eng.myls(4, 2)
# print(t)
# 调用MATLAB脚本
# eng.test1(nargout=0)
# eng.run('test1', nargout=0)

eng.main(nargout=0)
# 会把DLMP 和 Loadshedding的结果保存到文件夹中
