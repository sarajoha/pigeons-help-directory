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
        requests
        oyaml
        bs4
        pandas
        # selenium
        # pytest
        pyyaml
        jinja2
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
