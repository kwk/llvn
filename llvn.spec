# Use: https://www.redhat.com/en/blog/alternatives-command
# Weak Dependencies: https://docs.fedoraproject.org/en-US/packaging-guidelines/WeakDependencies/

%bcond_without no_more_compat_pkg

%global maj_ver 22
%global min_ver 0
%global patch_ver 0
%global maj_compat_ver %{lua: print(tonumber(rpm.expand('%maj_ver'))-1)}

Name:       llvn%{maj_ver}
Version:    %{maj_ver}.%{min_ver}.%{patch_ver}
Release:    25
Summary:    A demo for versioning llvn
License:    FIXME

# Alternative 1: Have compat version be optionally installable
%if %{with no_more_compat_pkg}
Obsoletes: llvn%{maj_compat_ver} < %{version}
%endif

# Alternative 2: Make compat version a requirement
# NOTE: The provides is a good idea to have anyway but it is needed for this in particular.
# Provides: %%{name}(major) = %%{maj_ver}
# %%if %%{with no_more_compat_pkg}
# Obsoletes: llvn%%{maj_compat_ver} < %%{version}
# %%else
# Requires: llvn%%{maj_compat_ver}(major) = %%{maj_compat_ver}
# %%endif

Requires(post): %{_sbindir}/update-alternatives
Requires(postun): %{_sbindir}/update-alternatives

%description
TBD.

%prep
# we have no source, so nothing here

%build
cat > hello-world-%{maj_ver}.sh <<EOF
#!/usr/bin/bash
echo "Hello World %{version}"
EOF

%install
%{__mkdir_p} %{buildroot}/usr/lib64/%{name}/bin
install -m 755 hello-world-%{maj_ver}.sh %{buildroot}/usr/lib64/%{name}/bin/hello-world-%{maj_ver}.sh

%{__mkdir_p} %{buildroot}%{_bindir}
# This is required (See https://docs.fedoraproject.org/en-US/packaging-guidelines/Alternatives/#_how_to_use_alternatives)
touch %{buildroot}%{_bindir}/hello-world.sh

%post
# Install alternative with: link name path priority
# Using the maj_ver as priority always prefers the newer llvm.
%{_sbindir}/update-alternatives \
    --verbose \
    --install \
        %{_bindir}/hello-world.sh \
        llvn \
        %{_libdir}/%{name}/bin/hello-world-%{maj_ver}.sh \
        %{maj_ver}

%postun
if [ $1 -eq 0 ] ; then
%{_sbindir}/update-alternatives \
    --verbose \
    --remove llvn %{_libdir}/%{name}/bin/hello-world-%{maj_ver}.sh
fi

%files
/usr/lib64/%{name}/bin/hello-world-%{maj_ver}.sh
# This is required (See https://docs.fedoraproject.org/en-US/packaging-guidelines/Alternatives/#_how_to_use_alternatives)
%ghost %{_bindir}/hello-world.sh

%changelog
%autochangelog
