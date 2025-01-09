import os
import subprocess
import platform


class ExecutionWorker():
    def __init__(self):
        pass

    def execute(self, id, batch_size, data_parallel_size):
        if platform.system() == 'Windows':
            exec_code = os.system(
                "cmake -B build ./ -DCMAKE_BUILD_TYPE=Release -B ./temp/EasySAT_{}".format((id-1) % batch_size))
            if exec_code != 0:
                return False

            for i in range(data_parallel_size):
                # argv id ���ĸ��ļ��� ���ݲ��е�index ���ݲ��д�С
                exec_code = os.system("start ./temp/EasySAT_{}/EasySAT.exe {} {} {}".format((id-1) % batch_size, id, data_parallel_size, i))
                # subprocess.call("start ./temp/EasySAT_{}/EasySAT.exe {} ./temp/EasySAT_{}/".format((id-1) % batch_size, id, (id-1) % batch_size))
                if exec_code != 0:
                    return False
            return True

        elif platform.system() == 'Linux':
            print(format((id - 1) % batch_size))
            exec_code = os.system(
                "cmake -DCMAKE_BUILD_TYPE=Release ./temp/EasySAT_{} -B ./temp/EasySAT_{}/build".format((id - 1) % batch_size,(id - 1) % batch_size))
            print(exec_code)
            if exec_code != 0:
                return False
            exec_code = os.system(
                "make -j  -C ./temp/EasySAT_{}/build".format((id - 1) % batch_size))
            if exec_code != 0:
                return False
            for i in range(data_parallel_size):
                exec_code = os.system(
                    "./temp/EasySAT_{}/build/lifelong --inputFile ./temp/EasySAT_{}/example_problems/random.domain/random_32_32_20_100.json -o test.json  &".format((id - 1) % batch_size,(id - 1) % batch_size))
                # subprocess.call("start ./temp/EasySAT_{}/EasySAT.exe {} ./temp/EasySAT_{}/".format((id-1) % batch_size, id, (id-1) % batch_size))
                if exec_code != 0:
                    return False
            return True

        else:
            raise ValueError("Unsupported this kind of system!")

    def execute_original(self, id, data_parallel_size):
        return self.execute(id=id, batch_size=1, data_parallel_size=data_parallel_size)

    def execute_eval(self,source_cpp_path, executable_file_path, data_parallel_size):
        id = 1 # only to occupy the position for parameters in EasySAT.cpp
        if platform.system() == 'Windows':
            exec_code = os.system(
                "g++ -O3 -Wall -std=c++17 {} -o {}".format( source_cpp_path, executable_file_path ) )
            if exec_code != 0:
                return False

            for i in range(data_parallel_size):
                exec_code = os.system("start {}.exe {} {} {}".format(executable_file_path, id, data_parallel_size, i))
                if exec_code != 0:
                    return False
            return True

        elif platform.system() == 'Linux':
            exec_code = os.system(
                "g++ -O3 -Wall -std=c++17 {} -o {}".format( source_cpp_path, executable_file_path ) )
            if exec_code != 0:
                return False

            for i in range(data_parallel_size):
                exec_code = os.system(
                    "{} {} {} {} &".format(executable_file_path, id, data_parallel_size, i)  )
                # subprocess.call("start ./temp/EasySAT_{}/EasySAT.exe {} ./temp/EasySAT_{}/".format((id-1) % batch_size, id, (id-1) % batch_size))
                if exec_code != 0:
                    return False
            return True

        else:
            raise ValueError("Unsupported this kind of system!")
