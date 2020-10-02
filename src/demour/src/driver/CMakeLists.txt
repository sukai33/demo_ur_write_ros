add_library(driver SHARED URDriver.cpp URScript.cpp utils.cpp)
target_link_libraries(
        driver
        Qt5::Core
        Qt5::Gui
        Qt5::Widgets
        Qt5::PrintSupport
        Qt5::Network
)