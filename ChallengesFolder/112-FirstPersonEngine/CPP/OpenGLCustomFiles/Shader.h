#pragma once

#include <GL/glew.h>
#include <GLFW/glfw3.h>

#include <iostream>
#include <fstream>
#include <string>

class Shader
{
private:
	unsigned int m_shaderID;

public:
	Shader();

	void bind();

	void newVFShader(const std::string& vertexName, const std::string& fragmentName);
	void compileShader(const GLuint type, const char* source, const std::string& shaderName);
	std::string getSourceFromFile(const std::string& shaderName, std::string& shaderRef);

	// Getters
	unsigned int getID();
};

std::string findShaderSourcePath();
