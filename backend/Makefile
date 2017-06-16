.PHONY: help, clean, install, dev

default: help

dev: clean
	python manage.py runserver

install:
	pip install -r requirements.txt

clean:
	@find . | grep -E "(__pycache__|\.pyc|\.pyo)$$" | xargs rm -rf

help:
	@echo "   \033[35mmake\033[0m \033[1m命令使用说明\033[0m"
	@echo "   \033[35mmake install\033[0m\t\033[0m\t---  安装依赖"
	@echo "   \033[35mmake dev\033[0m\t\033[0m\t---  开发模式"
	@echo "   \033[35mmake clean\033[0m\t\033[0m\t---  清理python缓存文件"
