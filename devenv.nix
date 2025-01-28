{ pkgs, ... }:

{

  # devcontainer.enable = true;

  packages = [
    # pkgs.chromedriver
    # pkgs.chromium
  ];

  languages.python = {
    enable = true;
    venv = {
      enable = true;
      requirements = ''
        bs4
        jinja2
        oyaml
        pandas
        pyyaml
        requests
        unidecode
      '';
    };
  };

  scripts = {
    create_readme.exec = ''
      pushd src > /dev/null &&
      python create_readme.py &&
      popd > /dev/null
    '';
  };
}
