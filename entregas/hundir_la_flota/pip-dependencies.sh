PACKAGE=$1
pip download $PACKAGE -d /tmp --no-binary :all: \
| grep Collecting \
| cut -d' ' -f2 \
| grep -Ev "$PACKAGE(~|=|\!|>|<|$)"

