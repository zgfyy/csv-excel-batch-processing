import configparser
from pathlib import Path

class Settings:
    _instance = None
    _config_path = Path("config/config.ini")

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Settings, cls).__new__(cls)
            cls._instance.load_config()
        return cls._instance

    def load_config(self):
        """加载配置文件"""
        self.config = configparser.ConfigParser()
        if self._config_path.exists():
            self.config.read(self._config_path)
        else:
            print(f"Warning: Config file {self._config_path} not found. Using default settings.")
            self.save_config()  # 创建默认配置文件

        self.load_default_settings()

    def save_config(self):
        """保存配置文件"""
        with open(self._config_path, 'w') as configfile:
            self.config.write(configfile)

    def load_default_settings(self):
        """加载默认设置"""
        self.input_directory = self.get_setting('DEFAULT', 'input_directory', './data/input')
        self.output_file = self.get_setting('DEFAULT', 'output_file', './data/output/merged_data.csv')
        self.key_columns = self.get_setting('DEFAULT', 'key_columns', '').split()
        self.skip_errors = self.get_setting('DEFAULT', 'skip_errors', 'True').lower() == 'true'
        self.overwrite_output = self.get_setting('DEFAULT', 'overwrite_output', 'False').lower() == 'true'
        self.custom_rules = self.load_custom_rules()

    def get_setting(self, section, option, default=None):
        """获取配置项，如果不存在则返回默认值"""
        try:
            return self.config.get(section, option)
        except (configparser.NoSectionError, configparser.NoOptionError):
            return default

    def set_setting(self, section, option, value):
        """设置配置项并保存"""
        if not self.config.has_section(section):
            self.config.add_section(section)
        self.config.set(section, option, str(value))
        self.save_config()

    def update_settings(self, settings_dict):
        """根据字典更新设置"""
        for key, value in settings_dict.items():
            setattr(self, key, value)
            self.set_setting('DEFAULT', key, value)

    def load_custom_rules(self):
        """加载自定义规则"""
        rules = []
        if 'CustomRules' in self.config:
            for key, value in self.config['CustomRules'].items():
                rule_parts = value.split()
                rule = {
                    'column': rule_parts[0],
                    'operation': rule_parts[1],
                    'params': {}
                }
                if len(rule_parts) > 2:
                    param_key, param_value = rule_parts[2].split('=')
                    rule['params'][param_key] = param_value
                rules.append(rule)
        return rules

    def save_custom_rules(self, rules):
        """保存自定义规则"""
        self.config.remove_section('CustomRules')
        self.config.add_section('CustomRules')
        for i, rule in enumerate(rules):
            rule_str = f"{rule['column']} {rule['operation']}"
            if 'type' in rule['params']:
                rule_str += f" type={rule['params']['type']}"
            if 'value' in rule['params']:
                rule_str += f" value={rule['params']['value']}"
            self.config.set('CustomRules', f"rule_{i}", rule_str)
        self.save_config()

# 初始化单例实例
settings = Settings()