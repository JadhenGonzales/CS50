#include "helpers.h"
#include <math.h>


int sobel(int matrix[3][3]);

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    int ave_RGB;
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            ave_RGB = round((image[i][j].rgbtBlue + image[i][j].rgbtGreen + image[i][j].rgbtRed) / 3.0);
            image[i][j].rgbtBlue = ave_RGB;
            image[i][j].rgbtGreen = ave_RGB;
            image[i][j].rgbtRed = ave_RGB;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE temp[width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            temp[width - j - 1] = image[i][j];
        }
        for (int j = 0; j < width; j++)
        {
            image[i][j] = temp[j];
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE temp_img[height][width];
    int box_size = 3;
    int sum[3];
    int values;

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            sum[0] = 0;
            sum[1] = 0;
            sum[2] = 0;
            values = 0;

            // get total sum of values in box
            for (int box_i = 0; box_i < box_size; box_i++)
            {
                for (int box_j = 0; box_j < box_size; box_j++)
                {
                    // account for edges and corners
                    if ((i + (box_i - 1)) >= 0 && (i + (box_i - 1)) < height && (j + (box_j - 1)) >= 0 && (j + (box_j - 1)) < width)
                    {
                        sum[0] += image[i + (box_i - 1)][j + (box_j - 1)].rgbtRed;
                        sum[1] += image[i + (box_i - 1)][j + (box_j - 1)].rgbtGreen;
                        sum[2] += image[i + (box_i - 1)][j + (box_j - 1)].rgbtBlue;
                        values += 1;
                    }
                }
            }

            // average and place int temp_img

            temp_img[i][j].rgbtRed = round(sum[0] / values);
            temp_img[i][j].rgbtGreen = round(sum[1] / values);
            temp_img[i][j].rgbtBlue = round(sum[2] / values);
        }
    }

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j] = temp_img[i][j];
        }
    }
    return;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE temp_img[height][width];
    int red[3][3];
    int green[3][3];
    int blue[3][3];

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            //Get 3x3 matrix of adjacents
            for (int matrix_i = 0; matrix_i < 3; matrix_i++)
            {
                for (int matrix_j = 0; matrix_j < 3; matrix_j++)
                {
                    // reset value to 0
                    red[matrix_i][matrix_j] = 0;
                    green[matrix_i][matrix_j] = 0;
                    blue[matrix_i][matrix_j] = 0;

                    // account for edges and corners
                    if ((i + (matrix_i - 1)) >= 0 && (i + (matrix_i - 1)) < height && (j + (matrix_j - 1)) >= 0 && (j + (matrix_j - 1)) < width)
                    {
                        red[matrix_i][matrix_j] = image[i + (matrix_i - 1)][j + (matrix_j - 1)].rgbtRed;
                        green[matrix_i][matrix_j] = image[i + (matrix_i - 1)][j + (matrix_j - 1)].rgbtGreen;
                        blue[matrix_i][matrix_j] = image[i + (matrix_i - 1)][j + (matrix_j - 1)].rgbtBlue;
                    }
                }
            }

            //sobel operation
            temp_img[i][j].rgbtRed = sobel(red);
            temp_img[i][j].rgbtGreen = sobel(green);
            temp_img[i][j].rgbtBlue = sobel(blue);
        }
    }

    // copy temp_img to image
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j] = temp_img[i][j];
        }
    }

    return;
}

int sobel(int matrix[3][3])
{
    int value_x = 0;
    int value_y = 0;

    // X-axis sobel operation
    value_x += (-matrix[0][0]);
    value_x += (-2 * matrix[1][0]);
    value_x += (-matrix[2][0]);

    value_x += (matrix[0][2]);
    value_x += (2 * matrix[1][2]);
    value_x += (matrix[2][2]);

    // Y-axis sobel operation
    value_y += (-matrix[0][0]);
    value_y += (-2 * matrix[0][1]);
    value_y += (-matrix[0][2]);

    value_y += (matrix[2][0]);
    value_y += (2 * matrix[2][1]);
    value_y += (matrix[2][2]);

    // Combine X and Y
    int value = round(sqrt((value_x * value_x) + (value_y * value_y)));

    if (value > 255)
    {
        value = 255;
    }
    else if (value < 0)
    {
        value = 0;
    }
    return value;
}
