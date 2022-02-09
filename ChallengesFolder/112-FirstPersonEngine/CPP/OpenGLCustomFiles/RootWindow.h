#pragma once

#include <assert.h>
#include <stdlib.h>

#include <GL/glew.h>
#include <GLFW/glfw3.h>

class RootWindow
{
private:
	GLFWwindow* window{};				// Pointer to window
	int winWidth{ 0 };					// Width of the screen
	int winHeight{ 0 };					// Height of the screen

public:
	// Constructor, create window
	RootWindow(
		const int& width,				// Window width
		const int& height,				// Window height
		const char* name,				// Window title
		GLFWmonitor* monitor = NULL,	// Monitor to appear on
		GLFWwindow* share = NULL		// Secondary window
	);

	// Get flag if window should close
	bool shouldClose();

	// Getter functions
	int getWindowWidth();
	int getWindowHeight();
	GLFWwindow* getWindow();
};
