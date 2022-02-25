CC=g++
CFLAGS=-c -pipe -O3

TARGET=btm
BUILD_DIR=.build
SOURCE_DIR=src

SOURCES=$(shell find $(SOURCE_DIR) -name '*.cpp')
OBJECTS=$(SOURCES:%=$(BUILD_DIR)/%.o)
DEPENDENCIES=$(OBJECTS:.o=.d)

CPPFLAGS=-MMD -MP

$(BUILD_DIR)/$(TARGET): $(OBJECTS)
	$(CC) $(OBJECTS) -o $@ $(LDFLAGS)

$(BUILD_DIR)/%.cpp.o: %.cpp
	@mkdir -p $(dir $@)
	$(CC) $(CPPFLAGS) $(CFLAGS) -c $< -o $@

PHONY: clean
clean:
	rm -rf $(BUILD_DIR)

-include $(DEPENDENCIES)

