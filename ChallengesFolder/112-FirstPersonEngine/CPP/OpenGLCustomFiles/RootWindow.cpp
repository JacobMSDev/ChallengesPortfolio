#include "RootWindow.h"

/*\
 * Setup the window using the specified arguments.
 * 
 * Close the program if something is not initialised
 * correctly.
 * (Plan to replace with log system)
\*/
RootWindow::RootWindow(
	const int& width, const int& height, const char* name,
	GLFWmonitor* monitor, GLFWwindow* share
)
{
	assert(glfwInit());

	window = glfwCreateWindow(width, height, name, monitor, share);
	if (!window) {
		glfwTerminate();
		exit(EXIT_FAILURE);
	}
	glfwMakeContextCurrent(window);

	winWidth = width;
	winHeight = height;

	glewInit();
}

/*\
 * Return the GLFW flag indicating if the
 * window should remain open or not.
\*/
bool RootWindow::shouldClose()
{
	return glfwWindowShouldClose(window);
}

/*\
 * Get the width of the window
\*/
int RootWindow::getWindowWidth()
{
	return winWidth;
}
/*\
 * Get the height of the window
\*/
int RootWindow::getWindowHeight()
{
	return winHeight;
}

/*\
 * Get the pointer to the window
\*/
GLFWwindow* RootWindow::getWindow()
{
	return window;
}
