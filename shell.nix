{pkgs ? import <nixpkgs> {}}:

pkgs.mkShell {
    buildInputs = with pkgs; [ 
        cargo
        rustc
        pkg-config
        openssl
        xorg.libX11
	xorg.libX11.dev
        xorg.libXcursor
        xorg.libXrandr
        xorg.libXi
        libGL
    ];

    shellHook = ''
      export LD_LIBRARY_PATH="${pkgs.xorg.libX11}/lib:${pkgs.xorg.libXcursor}/lib:${pkgs.xorg.libXrandr}/lib:${pkgs.xorg.libXi}/lib:${pkgs.libGL}/lib"
    '';
  }
